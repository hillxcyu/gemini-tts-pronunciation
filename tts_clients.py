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
"""Async synthesis clients for Vertex AI Gemini 3.8 TTS and Cloud TTS Chirp 3 HD.

Resolves GCP project settings from environment variables
(GOOGLE_CLOUD_PROJECT / GOOGLE_CLOUD_LOCATION='global') or active gcloud
configuration and executes authenticated synthesis calls via Application Default
Credentials.
"""

from __future__ import annotations

import asyncio
import base64
import configparser
import io
import os
from pathlib import Path
import time
from typing import Any
import wave

import google.auth
import google.auth.transport.requests
import httpx

CLOUD_PLATFORM_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]


def resolve_gcp_settings() -> dict[str, str]:
    """Resolves project_id, account, and location from env vars or gcloud config."""
    config_name = os.environ.get("GCLOUD_CONFIG_NAME") or os.environ.get(
        "CLOUDSDK_ACTIVE_CONFIG_NAME", "default"
    )
    cfg_path = (
        Path.home() / ".config" / "gcloud" / "configurations" / f"config_{config_name}"
    )
    cfg_project = ""
    cfg_account = ""
    if cfg_path.exists():
        parser = configparser.ConfigParser()
        parser.read(cfg_path, encoding="utf-8")
        cfg_project = parser.get("core", "project", fallback="").strip()
        cfg_account = parser.get("core", "account", fallback="").strip()

    if os.environ.get("K_SERVICE"):
        project_id = (
            os.environ.get("GOOGLE_CLOUD_PROJECT")
            or cfg_project
            or ""
        )
    else:
        project_id = (
            os.environ.get("GOOGLE_CLOUD_PROJECT")
            or cfg_project
            or ""
        )
    if not project_id:
        try:
            _, adc_project = google.auth.default(scopes=CLOUD_PLATFORM_SCOPES)
            if adc_project:
                project_id = str(adc_project)
        except Exception:
            project_id = ""
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global").strip() or "global"
    return {
        "gcloud_config": config_name,
        "project_id": project_id,
        "account": cfg_account or "ADC Service Account",
        "location": location,
    }


class GoogleAuthManager:
    """Thread/async-safe ADC bearer token provider bound to target quota project."""

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id
        self._creds: Any = None
        self._lock = asyncio.Lock()

    def _refresh_sync(self) -> str:
        if self._creds is None:
            creds, _ = google.auth.default(scopes=CLOUD_PLATFORM_SCOPES)
            if hasattr(creds, "with_quota_project"):
                creds = creds.with_quota_project(self.project_id)
            self._creds = creds
        if not self._creds.valid or self._creds.expired or not self._creds.token:
            self._creds.refresh(google.auth.transport.requests.Request())
        return str(self._creds.token)

    async def get_headers(self) -> dict[str, str]:
        async with self._lock:
            token = await asyncio.to_thread(self._refresh_sync)
        return {
            "Authorization": f"Bearer {token}",
            "x-goog-user-project": self.project_id,
            "Content-Type": "application/json",
        }


def ensure_wav_and_inspect(
    audio_bytes: bytes, fallback_sample_rate: int = 24000
) -> tuple[bytes, float, int]:
    """Ensures RIFF WAV container and extracts duration (seconds) & sample rate."""
    if not audio_bytes.startswith(b"RIFF"):
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fallback_sample_rate)
            wf.writeframes(audio_bytes)
        audio_bytes = buf.getvalue()

    with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate() or fallback_sample_rate
        duration = round(frames / float(rate), 2) if rate > 0 else 0.0
    return audio_bytes, duration, rate


class DualEngineTTSService:
    """Executes synthesis across Gemini 3.8 TTS and Chirp 3 HD."""

    def __init__(self) -> None:
        self.gcp = resolve_gcp_settings()
        self.project_id = self.gcp["project_id"]
        self.location = self.gcp["location"]
        self._auth = GoogleAuthManager(self.project_id)

    async def synthesize_gemini_tts(
        self,
        tts_transcript: str,
        language_code: str,
        voice_name: str = "Kore",
        model_id: str = "gemini-3.8-flash-tts",
        style: str = "",
    ) -> dict[str, Any]:
        """Synthesizes speech using Vertex AI Gemini 3.8 Flash / Flash-Lite TTS."""
        part: dict[str, Any] = {"text": tts_transcript}
        clean_style = style.strip()
        if clean_style:
            part["speechMetadata"] = {"style": clean_style}

        payload: dict[str, Any] = {
            "contents": [{"role": "user", "parts": [part]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "languageCode": language_code,
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {"voiceName": voice_name}
                    },
                },
            },
        }
        url = (
            f"https://aiplatform.googleapis.com/v1/projects/{self.project_id}"
            f"/locations/{self.location}/publishers/google/models/"
            f"{model_id}:generateContent"
        )

        headers = await self._auth.get_headers()
        t0 = time.perf_counter()
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
        latency_ms = round((time.perf_counter() - t0) * 1000.0, 1)

        if resp.status_code != 200:
            err_msg = _extract_api_error(resp)
            raise RuntimeError(
                f"Gemini 3.8 TTS ({model_id}) HTTP {resp.status_code}: {err_msg}"
            )

        data = resp.json()
        try:
            inline_data = data["candidates"][0]["content"]["parts"][0]["inlineData"]
            raw_audio = base64.b64decode(inline_data["data"])
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                f"Unexpected Gemini 3.8 TTS response structure: {data}"
            ) from exc

        wav_bytes, duration_s, sample_rate = ensure_wav_and_inspect(raw_audio)
        return {
            "engine": "gemini",
            "model": model_id,
            "voice": voice_name,
            "language_code": language_code,
            "mime_type": "audio/wav",
            "audio_base64": base64.b64encode(wav_bytes).decode("ascii"),
            "audio_size_bytes": len(wav_bytes),
            "duration_seconds": duration_s,
            "sample_rate_hz": sample_rate,
            "latency_ms": latency_ms,
            "applied_input": tts_transcript,
            "request_payload": payload,
        }

    async def synthesize_chirp3_hd(
        self,
        chirp_spec: dict[str, Any],
        speaking_rate: float = 1.0,
    ) -> dict[str, Any]:
        """Synthesizes speech using Cloud Text-to-Speech Chirp 3 HD."""
        effective_mode = chirp_spec.get("effective_mode", "ssml")
        input_obj: dict[str, Any] = {}

        if effective_mode == "ssml" and chirp_spec.get("ssml"):
            input_obj["ssml"] = chirp_spec["ssml"]
            applied_summary = chirp_spec["ssml"]
        else:
            input_obj["text"] = chirp_spec.get("text", "")
            applied_summary = input_obj["text"]
            custom_prons = chirp_spec.get("custom_pronunciations") or []
            if effective_mode == "custom_pronunciations" and custom_prons:
                input_obj["customPronunciations"] = {
                    "pronunciations": custom_prons
                }

        clamped_rate = max(0.25, min(2.0, float(speaking_rate)))
        payload: dict[str, Any] = {
            "input": input_obj,
            "voice": {
                "languageCode": chirp_spec["locale"],
                "name": chirp_spec["voice_name"],
            },
            "audioConfig": {
                "audioEncoding": "LINEAR16",
                "sampleRateHertz": 24000,
                "speakingRate": clamped_rate,
            },
        }
        url = "https://texttospeech.googleapis.com/v1beta1/text:synthesize"

        headers = await self._auth.get_headers()
        t0 = time.perf_counter()
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
        latency_ms = round((time.perf_counter() - t0) * 1000.0, 1)

        if resp.status_code != 200:
            err_msg = _extract_api_error(resp)
            raise RuntimeError(
                f"Chirp 3 HD ({chirp_spec['voice_name']}) HTTP {resp.status_code}: "
                f"{err_msg}"
            )

        data = resp.json()
        audio_b64 = data.get("audioContent")
        if not audio_b64:
            raise RuntimeError(f"Missing audioContent in Chirp 3 HD response: {data}")

        raw_audio = base64.b64decode(audio_b64)
        wav_bytes, duration_s, sample_rate = ensure_wav_and_inspect(raw_audio)
        return {
            "engine": "chirp3_hd",
            "model": chirp_spec["voice_name"],
            "voice": chirp_spec["voice_name"],
            "language_code": chirp_spec["locale"],
            "effective_control_mode": effective_mode,
            "mime_type": "audio/wav",
            "audio_base64": base64.b64encode(wav_bytes).decode("ascii"),
            "audio_size_bytes": len(wav_bytes),
            "duration_seconds": duration_s,
            "sample_rate_hz": sample_rate,
            "latency_ms": latency_ms,
            "applied_input": applied_summary,
            "custom_pronunciations": chirp_spec.get("custom_pronunciations", []),
            "request_payload": payload,
        }


def _extract_api_error(resp: httpx.Response) -> str:
    try:
        body = resp.json()
        if isinstance(body, dict) and "error" in body:
            err = body["error"]
            if isinstance(err, dict):
                return str(err.get("message") or err)
            return str(err)
    except ValueError:
        pass
    return resp.text[:400]
