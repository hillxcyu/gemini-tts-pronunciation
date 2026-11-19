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
"""Multilingual custom terminology & phonetic compiler for Gemini 3.8 TTS & Chirp 3 HD.

Compiles clean display text into:
1. Gemini 3.8 TTS dual-track transcripts (`tts_transcript` + `speechMetadata.style`
   + optional English `<short pause>` tags), enforcing verbatim prefill safety.
2. Chirp 3 HD structured phonetic payloads, supporting both synchronous SSML
   (`<speak>` with `<phoneme>`, `<say-as>`, `<sub>`, and cross-lingual `<voice>`)
   and `CustomPronunciations` (`PHONETIC_ENCODING_IPA` / `X_SAMPA` for es/pt,
   and mandatory `PHONETIC_ENCODING_PINYIN` for cmn-CN).
"""

from __future__ import annotations

import html
import re
from typing import Any

from glossary_data import DEFAULT_GLOSSARY, LANGUAGES


def resolve_lang_family(language_code: str) -> str:
    """Maps a BCP-47 language code to 'es', 'pt', or 'zh'."""
    norm = language_code.strip().lower().replace("_", "-")
    if norm.startswith("es"):
        return "es"
    if norm.startswith("pt"):
        return "pt"
    if norm.startswith(("cmn", "zh")):
        return "zh"
    return "es"


def resolve_chirp_locale(
    language_code: str,
) -> tuple[str, str | None, str | None]:
    """Resolves the supported Chirp 3 HD locale and bilingual fallback notes."""
    for lang in LANGUAGES:
        for loc in lang["locales"]:
            if loc["code"].lower() == language_code.lower():
                return (
                    loc["chirp_locale"],
                    loc.get("chirp_fallback_note"),
                    loc.get("chirp_fallback_note_zh"),
                )
    fam = resolve_lang_family(language_code)
    if fam == "pt":
        return "pt-BR", None, None
    if fam == "zh":
        return "cmn-CN", None, None
    return "es-ES", None, None


def _is_ascii_word_char(ch: str) -> bool:
    return ch.isascii() and (ch.isalnum() or ch == "_")


def _build_term_pattern(term: str) -> re.Pattern[str]:
    """Builds a case-insensitive matcher safe across Latin and CJK scripts."""
    escaped = re.escape(term)
    # Allow flexible whitespace inside multi-word terms like 'Voltara EX2'
    escaped = escaped.replace(r"\ ", r"\s+")
    starts_ascii = _is_ascii_word_char(term[0])
    ends_ascii = _is_ascii_word_char(term[-1])
    prefix = r"(?<![A-Za-z0-9_])" if starts_ascii else ""
    suffix = r"(?![A-Za-z0-9_])" if ends_ascii else ""
    return re.compile(f"{prefix}{escaped}{suffix}", re.IGNORECASE)


def _select_native_rule(
    entry: dict[str, Any], language_code: str, lang_family: str
) -> dict[str, Any] | None:
    """Selects the most specific native-language rule for a glossary item."""
    native_map = entry.get("native") or {}
    if language_code in native_map:
        return native_map[language_code]
    for k, v in native_map.items():
        if k.lower() == language_code.lower():
            return v
    if lang_family in native_map:
        return native_map[lang_family]
    return None


def _build_english_ssml_fragment(
    entry: dict[str, Any], matched_surface: str, voice_name: str, chirp_locale: str
) -> str:
    """Builds a Chirp 3 HD SSML fragment for Standard English mode."""
    eng = entry.get("english") or {}
    has_cjk = any("\u4e00" <= ch <= "\u9fff" for ch in matched_surface)
    if has_cjk and not eng.get("chirp_ipa_en"):
        return html.escape(eng.get("gemini", matched_surface))

    inner = eng.get("chirp_ssml")
    if not inner:
        ipa_en = eng.get("chirp_ipa_en") or eng.get("chirp_ipa")
        if ipa_en:
            safe_ph = html.escape(ipa_en, quote=True)
            inner = (
                f'<phoneme alphabet="ipa" ph="{safe_ph}">'
                f"{html.escape(matched_surface)}</phoneme>"
            )
        else:
            alias = html.escape(eng.get("gemini", matched_surface), quote=True)
            inner = f'<sub alias="{alias}">{html.escape(matched_surface)}</sub>'

    en_voice = f"en-US-Chirp3-HD-{voice_name}"
    if chirp_locale.lower() == "en-us":
        return inner
    return f'<voice name="{en_voice}">{inner}</voice>'


def _build_native_ssml_fragment(
    native_rule: dict[str, Any], matched_surface: str
) -> str:
    """Builds a Chirp 3 HD SSML fragment for Native Language mode."""
    if native_rule.get("chirp_ssml"):
        return native_rule["chirp_ssml"]
    if native_rule.get("chirp_ipa"):
        safe_ph = html.escape(native_rule["chirp_ipa"], quote=True)
        return (
            f'<phoneme alphabet="ipa" ph="{safe_ph}">'
            f"{html.escape(matched_surface)}</phoneme>"
        )
    alias = html.escape(native_rule.get("gemini", matched_surface), quote=True)
    return f'<sub alias="{alias}">{html.escape(matched_surface)}</sub>'


def compile_pronunciation(
    text: str,
    language_code: str = "es-ES",
    pronunciation_mode: str = "english",
    voice_name: str = "Kore",
    chirp_control_mode: str = "ssml",
    insert_pauses: bool = False,
    glossary: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compiles source text into Gemini 3.8 TTS and Chirp 3 HD inputs.

    Args:
        text: User-facing display text.
        language_code: BCP-47 locale ('es-ES', 'es-US', 'pt-BR', 'pt-PT', 'cmn-CN').
        pronunciation_mode: 'english' (Standard English), 'native' (Localized),
            or 'raw' (Uncontrolled baseline).
        voice_name: Shared prebuilt voice persona (e.g., 'Kore', 'Puck').
        chirp_control_mode: 'ssml' or 'custom_pronunciations'.
        insert_pauses: Whether to inject micro-pauses before technical spans.
        glossary: Optional custom glossary list overriding DEFAULT_GLOSSARY.

    Returns:
        Dictionary with Gemini 3.8 transcript, Chirp 3 HD input spec, matched
        spans, and diagnostic notes.
    """
    active_glossary = glossary if glossary is not None else DEFAULT_GLOSSARY
    lang_family = resolve_lang_family(language_code)
    chirp_locale, chirp_fallback_note, chirp_fallback_note_zh = (
        resolve_chirp_locale(language_code)
    )
    chirp_voice_name = f"{chirp_locale}-Chirp3-HD-{voice_name}"

    notes: list[str] = []
    notes_zh: list[str] = []
    if chirp_fallback_note:
        notes.append(chirp_fallback_note)
    if chirp_fallback_note_zh:
        notes_zh.append(chirp_fallback_note_zh)

    if pronunciation_mode == "raw":
        return {
            "display_text": text,
            "language_code": language_code,
            "pronunciation_mode": "raw",
            "matched_terms": [],
            "gemini": {
                "tts_transcript": text,
                "language_code": language_code,
                "voice_name": voice_name,
            },
            "chirp": {
                "effective_mode": "text",
                "locale": chirp_locale,
                "voice_name": chirp_voice_name,
                "text": text,
                "ssml": None,
                "custom_pronunciations": [],
            },
            "notes": notes
            + [
                "Raw baseline active: sending unmodified text to both engines "
                "without glossary or phonetic overrides."
            ],
            "notes_zh": notes_zh
            + [
                "当前为原始未控基线模式：直接向双引擎发送未经改写的原始文本，不启用自定义词表或音素干预。"
            ],
        }

    # Filter enabled entries with non-empty terms, sorted longest-first so
    # 'Voltara EX2' matches ahead of 'Voltara'.
    enabled_entries = [
        e
        for e in active_glossary
        if e.get("enabled", True) and str(e.get("term", "")).strip()
    ]
    enabled_entries.sort(key=lambda e: len(str(e["term"]).strip()), reverse=True)

    # Find non-overlapping matches across `text`
    occupied = [False] * len(text)
    raw_matches: list[dict[str, Any]] = []

    for entry in enabled_entries:
        term = str(entry["term"]).strip()
        if pronunciation_mode == "native":
            rule_check = _select_native_rule(entry, language_code, lang_family)
            if not rule_check:
                continue
        pattern = _build_term_pattern(term)
        for m in pattern.finditer(text):
            start, end = m.span()
            if start == end or any(occupied[start:end]):
                continue
            for idx in range(start, end):
                occupied[idx] = True
            raw_matches.append(
                {
                    "start": start,
                    "end": end,
                    "surface": m.group(0),
                    "entry": entry,
                }
            )

    raw_matches.sort(key=lambda item: item["start"])

    # Assemble Gemini 3.8 transcript, Chirp SSML, and Chirp CustomPronunciations
    gemini_parts: list[str] = []
    ssml_parts: list[str] = ["<speak>"]
    chirp_text_parts: list[str] = []
    custom_prons_by_phrase: dict[str, dict[str, str]] = {}
    matched_terms_summary: list[dict[str, Any]] = []

    cursor = 0
    zh_english_requires_ssml = False

    for match in raw_matches:
        start, end = match["start"], match["end"]
        surface = match["surface"]
        entry = match["entry"]

        prefix_plain = text[cursor:start]
        gemini_parts.append(prefix_plain)
        ssml_parts.append(html.escape(prefix_plain))
        chirp_text_parts.append(prefix_plain)

        if pronunciation_mode == "english":
            eng_rule = entry.get("english") or {}
            gemini_rep = eng_rule.get("gemini", surface)
            ssml_frag = _build_english_ssml_fragment(
                entry, surface, voice_name, chirp_locale
            )
            chirp_text_parts.append(surface)

            if lang_family in ("es", "pt"):
                ipa_key = f"chirp_ipa_{lang_family}"
                ipa_val = (
                    eng_rule.get(ipa_key)
                    or eng_rule.get("chirp_ipa")
                    or eng_rule.get("chirp_ipa_en")
                )
                encoding = eng_rule.get(
                    "chirp_encoding", "PHONETIC_ENCODING_IPA"
                )
                if ipa_val:
                    custom_prons_by_phrase[surface.lower()] = {
                        "phrase": surface,
                        "phoneticEncoding": encoding,
                        "pronunciation": ipa_val,
                    }
            elif lang_family == "zh":
                has_cjk = any("\u4e00" <= ch <= "\u9fff" for ch in surface)
                if not has_cjk:
                    zh_english_requires_ssml = True
            applied_phonetic = (
                eng_rule.get("chirp_ipa_en")
                or eng_rule.get(f"chirp_ipa_{lang_family}")
                or ssml_frag
            )
        else:
            native_rule = (
                _select_native_rule(entry, language_code, lang_family) or {}
            )
            gemini_rep = native_rule.get("gemini", surface)
            ssml_frag = _build_native_ssml_fragment(native_rule, surface)

            if lang_family == "zh":
                sub_text = native_rule.get("chirp_text_sub", gemini_rep)
                chirp_text_parts.append(sub_text)
                pinyin_val = native_rule.get("chirp_pinyin")
                pinyin_phrase = native_rule.get("chirp_pinyin_phrase", sub_text)
                if pinyin_val and pinyin_phrase:
                    custom_prons_by_phrase[pinyin_phrase.lower()] = {
                        "phrase": pinyin_phrase,
                        "phoneticEncoding": "PHONETIC_ENCODING_PINYIN",
                        "pronunciation": pinyin_val,
                    }
                applied_phonetic = (
                    f"PINYIN: {pinyin_val}" if pinyin_val else sub_text
                )
            else:
                chirp_text_parts.append(surface)
                ipa_val = native_rule.get("chirp_ipa")
                encoding = native_rule.get(
                    "chirp_encoding", "PHONETIC_ENCODING_IPA"
                )
                if ipa_val:
                    custom_prons_by_phrase[surface.lower()] = {
                        "phrase": surface,
                        "phoneticEncoding": encoding,
                        "pronunciation": ipa_val,
                    }
                applied_phonetic = ipa_val or ssml_frag

        if insert_pauses and cursor > 0:
            gemini_parts.append("<short pause> ")
            ssml_parts.append('<break time="120ms"/>')

        gemini_parts.append(gemini_rep)
        ssml_parts.append(ssml_frag)

        matched_terms_summary.append(
            {
                "term": entry["term"],
                "surface": surface,
                "start": start,
                "end": end,
                "category": entry.get("category", "terminology"),
                "gemini_replacement": gemini_rep,
                "chirp_phonetic": applied_phonetic,
                "chirp_ssml": ssml_frag,
            }
        )
        cursor = end

    tail_plain = text[cursor:]
    gemini_parts.append(tail_plain)
    ssml_parts.append(html.escape(tail_plain))
    chirp_text_parts.append(tail_plain)
    ssml_parts.append("</speak>")

    gemini_transcript = "".join(gemini_parts)
    ssml_doc = "".join(ssml_parts)
    chirp_plain_text = "".join(chirp_text_parts)
    custom_prons_list = list(custom_prons_by_phrase.values())

    effective_chirp_mode = chirp_control_mode
    if (
        chirp_control_mode == "custom_pronunciations"
        and lang_family == "zh"
        and pronunciation_mode == "english"
        and zh_english_requires_ssml
    ):
        effective_chirp_mode = "ssml"
        notes.append(
            "Chirp 3 HD cmn-CN CustomPronunciations strictly accepts "
            "PHONETIC_ENCODING_PINYIN; switched Chirp 3 HD to SSML "
            "<voice name=\"en-US-Chirp3-HD-...\"> for Standard English phonemes."
        )
        notes_zh.append(
            "Chirp 3 HD 的 cmn-CN CustomPronunciations 接口仅支持拼音编码 "
            "(PHONETIC_ENCODING_PINYIN)；已自动切换为 SSML "
            "<voice name=\"en-US-Chirp3-HD-...\"> 以实现标准英语音素发音。"
        )

    return {
        "display_text": text,
        "language_code": language_code,
        "pronunciation_mode": pronunciation_mode,
        "matched_terms": matched_terms_summary,
        "gemini": {
            "tts_transcript": gemini_transcript,
            "language_code": language_code,
            "voice_name": voice_name,
        },
        "chirp": {
            "requested_mode": chirp_control_mode,
            "effective_mode": effective_chirp_mode,
            "locale": chirp_locale,
            "voice_name": chirp_voice_name,
            "text": chirp_plain_text,
            "ssml": ssml_doc,
            "custom_pronunciations": custom_prons_list,
        },
        "notes": notes,
        "notes_zh": notes_zh,
    }
