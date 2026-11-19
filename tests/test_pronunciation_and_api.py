# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit and live API integration tests for the Multilingual Pronunciation Studio.

Verifies pronunciation compilation across Spanish, Portuguese, and Chinese in
Standard English, Native Language, and Raw modes, plus FastAPI endpoints and
live synthesis against Gemini 3.8 TTS and Chirp 3 HD using Application Default
Credentials.
"""

from __future__ import annotations

import base64
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient  # noqa: E402

import app as web_app  # noqa: E402
from pronunciation_engine import compile_pronunciation  # noqa: E402


class PronunciationCompilerTest(unittest.TestCase):
    """Tests dual-track Gemini 3.8 and Chirp 3 HD phonetic compilation."""

    def test_spanish_voltara_ex2_english_vs_native_vs_raw(self) -> None:
        sample = "Descubre el nuevo Voltara Ex2, el SUV con actualizaciones OTA."

        # 1. Standard English mode
        eng = compile_pronunciation(
            text=sample,
            language_code="es-ES",
            pronunciation_mode="english",
            voice_name="Kore",
            chirp_control_mode="ssml",
        )
        self.assertIn("Vol-tah-rah E-X two", eng["gemini"]["tts_transcript"])
        self.assertIn("S-U-V", eng["gemini"]["tts_transcript"])
        self.assertIn("O-T-A", eng["gemini"]["tts_transcript"])
        self.assertIn(
            '<voice name="en-US-Chirp3-HD-Kore">', eng["chirp"]["ssml"]
        )
        self.assertEqual(len(eng["matched_terms"]), 3)
        # Ensure longest-match 'Voltara Ex2' matched as one span, not split
        self.assertEqual(eng["matched_terms"][0]["surface"], "Voltara Ex2")

        # 2. Native Language mode (Spanish)
        nat = compile_pronunciation(
            text=sample,
            language_code="es-ES",
            pronunciation_mode="native",
            voice_name="Puck",
            chirp_control_mode="custom_pronunciations",
        )
        self.assertIn("Bol-ta-ra E equis dos", nat["gemini"]["tts_transcript"])
        self.assertIn("ese u uve", nat["gemini"]["tts_transcript"])
        self.assertEqual(nat["chirp"]["voice_name"], "es-ES-Chirp3-HD-Puck")
        phrases = {
            p["phrase"]: p["pronunciation"]
            for p in nat["chirp"]["custom_pronunciations"]
        }
        self.assertIn("Voltara Ex2", phrases)

        # 3. Raw baseline mode
        raw = compile_pronunciation(
            text=sample,
            language_code="es-ES",
            pronunciation_mode="raw",
            voice_name="Kore",
        )
        self.assertEqual(raw["gemini"]["tts_transcript"], sample)
        self.assertEqual(raw["matched_terms"], [])

    def test_portuguese_pt_pt_chirp_locale_mapping(self) -> None:
        res = compile_pronunciation(
            text="Conheça o novo Voltara EX2, o SUV urbano.",
            language_code="pt-PT",
            pronunciation_mode="native",
            voice_name="Aoede",
        )
        self.assertEqual(res["gemini"]["language_code"], "pt-PT")
        self.assertEqual(res["chirp"]["locale"], "pt-BR")
        self.assertIn("Vol-tá-ra É xis dois", res["gemini"]["tts_transcript"])
        self.assertTrue(any("pt-BR" in n for n in res["notes"]))

    def test_chinese_pinyin_and_english_ssml_fallback(self) -> None:
        sample = "欢迎体验全新 Voltara Ex2 智能纯电 SUV，经过银行路口。"

        # Native Mandarin mode uses PHONETIC_ENCODING_PINYIN
        nat_zh = compile_pronunciation(
            text=sample,
            language_code="cmn-CN",
            pronunciation_mode="native",
            voice_name="Kore",
            chirp_control_mode="custom_pronunciations",
        )
        self.assertIn("沃尔塔拉 E-X 二", nat_zh["gemini"]["tts_transcript"])
        encodings = {
            p["phoneticEncoding"]
            for p in nat_zh["chirp"]["custom_pronunciations"]
        }
        self.assertEqual(encodings, {"PHONETIC_ENCODING_PINYIN"})

        # Standard English mode on cmn-CN switches CustomPronunciations -> SSML
        eng_zh = compile_pronunciation(
            text=sample,
            language_code="cmn-CN",
            pronunciation_mode="english",
            voice_name="Kore",
            chirp_control_mode="custom_pronunciations",
        )
        self.assertEqual(eng_zh["chirp"]["effective_mode"], "ssml")
        self.assertIn(
            '<voice name="en-US-Chirp3-HD-Kore">', eng_zh["chirp"]["ssml"]
        )


class LiveWebAppIntegrationTest(unittest.TestCase):
    """End-to-end FastAPI + live Vertex AI / Cloud TTS verification."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(web_app.app)

    def test_health_and_config_and_index(self) -> None:
        r_health = self.client.get("/healthz")
        self.assertEqual(r_health.status_code, 200)
        self.assertTrue(bool(r_health.json()["gcp"]["project_id"]))
        self.assertEqual(r_health.json()["gcp"]["location"], "global")

        r_cfg = self.client.get("/api/config")
        self.assertEqual(r_cfg.status_code, 200)
        cfg = r_cfg.json()
        self.assertEqual([l["id"] for l in cfg["languages"]], ["es", "pt", "zh"])
        self.assertTrue(all("label_zh" in l for l in cfg["languages"]))
        self.assertTrue(all("character_zh" in v for v in cfg["voices"]))
        self.assertGreaterEqual(len(cfg["voices"]), 10)

        r_idx = self.client.get("/")
        self.assertEqual(r_idx.status_code, 200)
        self.assertIn(
            "Multilingual &amp; Custom Terminology Pronunciation Studio", r_idx.text
        )
        self.assertIn('id="ui-lang-en"', r_idx.text)
        self.assertIn('id="ui-lang-zh"', r_idx.text)

        r_prev = self.client.post(
            "/api/preview",
            json={
                "text": "欢迎体验 Voltara Ex2",
                "language_code": "cmn-CN",
                "pronunciation_mode": "english",
                "voice_name": "Kore",
                "chirp_control_mode": "custom_pronunciations",
            },
        )
        self.assertEqual(r_prev.status_code, 200)
        self.assertTrue(len(r_prev.json().get("notes_zh", [])) > 0)

    def test_live_spanish_compare_english_and_native_custom_prons(self) -> None:
        # 1. Spanish + English Brand Names (Standard English Mode, SSML)
        r_en = self.client.post(
            "/api/synthesize",
            json={
                "text": "Descubre el nuevo Voltara Ex2, el SUV con Apple CarPlay y OTA.",
                "language_code": "es-ES",
                "pronunciation_mode": "english",
                "voice_name": "Kore",
                "chirp_control_mode": "ssml",
                "engine": "compare",
                "gemini_model": "gemini-3.8-flash-tts",
                "style": "Warm automotive commercial presenter.",
                "speaking_rate": 1.0,
            },
        )
        self.assertEqual(r_en.status_code, 200, r_en.text)
        body_en = r_en.json()
        self.assertEqual(body_en["errors"], {})
        self.assertIn("gemini", body_en["results"])
        self.assertIn("chirp3_hd", body_en["results"])

        # Validate both WAV outputs via ffprobe
        with tempfile.TemporaryDirectory() as tmpdir:
            for key in ("gemini", "chirp3_hd"):
                wav_bytes = base64.b64decode(body_en["results"][key]["audio_base64"])
                self.assertTrue(wav_bytes.startswith(b"RIFF"))
                wav_path = Path(tmpdir) / f"{key}.wav"
                wav_path.write_bytes(wav_bytes)
                probe = subprocess.run(
                    [
                        "ffprobe",
                        "-v",
                        "error",
                        "-show_entries",
                        "stream=codec_name,sample_rate,channels",
                        "-of",
                        "default=noprint_wrappers=1",
                        str(wav_path),
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.assertIn("codec_name=pcm_s16le", probe.stdout)
                self.assertIn("sample_rate=24000", probe.stdout)

        # 2. Spanish Native Mode with Chirp 3 HD CustomPronunciations IPA
        r_nat = self.client.post(
            "/api/synthesize",
            json={
                "text": "Descubre el nuevo Voltara Ex2, el SUV con LiDAR y OTA.",
                "language_code": "es-ES",
                "pronunciation_mode": "native",
                "voice_name": "Puck",
                "chirp_control_mode": "custom_pronunciations",
                "engine": "compare",
                "gemini_model": "gemini-3.8-flash-lite-tts",
                "speaking_rate": 1.0,
            },
        )
        self.assertEqual(r_nat.status_code, 200, r_nat.text)
        self.assertEqual(r_nat.json()["errors"], {})

    def test_live_portuguese_and_chinese_custom_prons(self) -> None:
        # Portuguese Native CustomPronunciations IPA
        r_pt = self.client.post(
            "/api/synthesize",
            json={
                "text": "Conheça o novo Voltara Ex2, o SUV com LiDAR e OTA.",
                "language_code": "pt-BR",
                "pronunciation_mode": "native",
                "voice_name": "Aoede",
                "chirp_control_mode": "custom_pronunciations",
                "engine": "chirp3_hd",
            },
        )
        self.assertEqual(r_pt.status_code, 200, r_pt.text)
        self.assertEqual(r_pt.json()["errors"], {})

        # Chinese Native CustomPronunciations PINYIN + Gemini 3.8 Flash TTS
        r_zh = self.client.post(
            "/api/synthesize",
            json={
                "text": "欢迎体验全新 Voltara Ex2 智能纯电 SUV，经过银行路口。",
                "language_code": "cmn-CN",
                "pronunciation_mode": "native",
                "voice_name": "Kore",
                "chirp_control_mode": "custom_pronunciations",
                "engine": "compare",
                "gemini_model": "gemini-3.8-flash-tts",
            },
        )
        self.assertEqual(r_zh.status_code, 200, r_zh.text)
        self.assertEqual(r_zh.json()["errors"], {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
