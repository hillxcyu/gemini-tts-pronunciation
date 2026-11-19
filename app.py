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
"""FastAPI backend for the Multilingual & Custom Terminology Pronunciation Studio.

Exposes configuration, real-time dual-track/phonetic compilation preview, and
single or parallel side-by-side synthesis across Gemini 3.8 TTS and Chirp 3 HD.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from glossary_data import DEFAULT_GLOSSARY, LANGUAGES, PREBUILT_VOICES, PRESET_SCRIPTS
from pronunciation_engine import compile_pronunciation
from tts_clients import DualEngineTTSService

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Multilingual & Custom Terminology Pronunciation Studio",
    description=(
        "Interactive comparison & control workbench for Gemini 3.8 TTS "
        "(Vertex AI global) and Chirp 3 HD (Cloud Text-to-Speech)."
    ),
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

tts_service = DualEngineTTSService()


@app.exception_handler(HTTPException)
async def http_exception_json_handler(
    _request: Request, exc: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def unhandled_exception_json_handler(
    _request: Request, exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {exc}"},
    )


class PreviewRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2500)
    language_code: str = Field(default="es-ES")
    pronunciation_mode: Literal["english", "native", "raw"] = Field(default="english")
    voice_name: str = Field(default="Kore")
    chirp_control_mode: Literal["ssml", "custom_pronunciations"] = Field(
        default="ssml"
    )
    insert_pauses: bool = Field(default=False)
    glossary: list[dict[str, Any]] | None = Field(default=None)


class SynthesizeRequest(PreviewRequest):
    engine: Literal["compare", "gemini", "chirp3_hd"] = Field(default="compare")
    gemini_model: Literal["gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts"] = Field(
        default="gemini-3.8-flash-tts"
    )
    style: str = Field(default="")
    speaking_rate: float = Field(default=1.0, ge=0.5, le=2.0)


@app.get("/healthz")
async def healthz() -> dict[str, Any]:
    return {
        "status": "ok",
        "gcp": tts_service.gcp,
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/api/config")
async def get_config() -> dict[str, Any]:
    return {
        "gcp": tts_service.gcp,
        "languages": LANGUAGES,
        "voices": PREBUILT_VOICES,
        "presets": PRESET_SCRIPTS,
        "default_glossary": DEFAULT_GLOSSARY,
        "gemini_models": [
            {
                "id": "gemini-3.8-flash-tts",
                "label": "Gemini 3.8 Flash TTS (Flagship · 130 Languages)",
                "label_zh": "Gemini 3.8 Flash TTS（旗舰音质 · 支持 130 种语言）",
            },
            {
                "id": "gemini-3.8-flash-lite-tts",
                "label": "Gemini 3.8 Flash-Lite TTS (Low Latency · 101 Languages)",
                "label_zh": "Gemini 3.8 Flash-Lite TTS（低延迟生产级 · 支持 101 种语言）",
            },
        ],
    }


@app.post("/api/preview")
async def preview_compilation(req: PreviewRequest) -> dict[str, Any]:
    return compile_pronunciation(
        text=req.text,
        language_code=req.language_code,
        pronunciation_mode=req.pronunciation_mode,
        voice_name=req.voice_name,
        chirp_control_mode=req.chirp_control_mode,
        insert_pauses=req.insert_pauses,
        glossary=req.glossary,
    )


@app.post("/api/synthesize")
async def synthesize(req: SynthesizeRequest) -> dict[str, Any]:
    compiled = compile_pronunciation(
        text=req.text,
        language_code=req.language_code,
        pronunciation_mode=req.pronunciation_mode,
        voice_name=req.voice_name,
        chirp_control_mode=req.chirp_control_mode,
        insert_pauses=req.insert_pauses,
        glossary=req.glossary,
    )

    results: dict[str, Any] = {}
    errors: dict[str, str] = {}

    async def _run_gemini() -> None:
        try:
            results["gemini"] = await tts_service.synthesize_gemini_tts(
                tts_transcript=compiled["gemini"]["tts_transcript"],
                language_code=req.language_code,
                voice_name=req.voice_name,
                model_id=req.gemini_model,
                style=req.style,
            )
        except Exception as exc:  # pylint: disable=broad-except
            errors["gemini"] = str(exc)

    async def _run_chirp() -> None:
        try:
            results["chirp3_hd"] = await tts_service.synthesize_chirp3_hd(
                chirp_spec=compiled["chirp"],
                speaking_rate=req.speaking_rate,
            )
        except Exception as exc:  # pylint: disable=broad-except
            errors["chirp3_hd"] = str(exc)

    tasks = []
    if req.engine in ("compare", "gemini"):
        tasks.append(_run_gemini())
    if req.engine in ("compare", "chirp3_hd"):
        tasks.append(_run_chirp())

    await asyncio.gather(*tasks)

    if not results and errors:
        detail = "; ".join(f"{k}: {v}" for k, v in errors.items())
        raise HTTPException(status_code=502, detail=detail)

    return {
        "compiled": compiled,
        "results": results,
        "errors": errors,
    }
