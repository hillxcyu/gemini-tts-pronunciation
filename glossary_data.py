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
"""Curated multilingual voices, sample scripts, and custom pronunciation glossary.

Provides language definitions (Spanish, Portuguese, Chinese), shared prebuilt
voice personas for Gemini 3.8 TTS and Chirp 3 HD, code-switching sample scripts
headlined by 'Voltara EX2', bidirectional pronunciation rules ('english' vs.
'native'), and bilingual UI metadata (English & Simplified Chinese).
All IPA and Pinyin strings are verified against Cloud TTS Chirp 3 HD Greco
phoneme validation across es-ES, es-US, pt-BR, and cmn-CN.
"""

from __future__ import annotations

from typing import Any

LANGUAGES: list[dict[str, Any]] = [
    {
        "id": "es",
        "label": "Spanish (Español)",
        "label_zh": "西班牙语 (Español)",
        "default_locale": "es-ES",
        "locales": [
            {
                "code": "es-ES",
                "label": "Español (España) — es-ES",
                "label_zh": "西班牙语（西班牙）— es-ES",
                "chirp_locale": "es-ES",
                "chirp_custom_encoding": "IPA",
            },
            {
                "code": "es-US",
                "label": "Español (EE. UU. / Latinoamérica) — es-US",
                "label_zh": "西班牙语（美国 / 拉美）— es-US",
                "chirp_locale": "es-US",
                "chirp_custom_encoding": "IPA",
            },
        ],
        "default_style": (
            "Warm, polished commercial automotive narrator with clear diction."
        ),
    },
    {
        "id": "pt",
        "label": "Portuguese (Português)",
        "label_zh": "葡萄牙语 (Português)",
        "default_locale": "pt-BR",
        "locales": [
            {
                "code": "pt-BR",
                "label": "Português (Brasil) — pt-BR",
                "label_zh": "葡萄牙语（巴西）— pt-BR",
                "chirp_locale": "pt-BR",
                "chirp_custom_encoding": "IPA",
            },
            {
                "code": "pt-PT",
                "label": "Português (Portugal) — pt-PT",
                "label_zh": "葡萄牙语（葡萄牙）— pt-PT",
                "chirp_locale": "pt-BR",
                "chirp_fallback_note": (
                    "Chirp 3 HD maps pt-PT to pt-BR; Gemini 3.8 TTS natively "
                    "supports pt-PT."
                ),
                "chirp_fallback_note_zh": (
                    "Chirp 3 HD 将 pt-PT 自动映射至 pt-BR 音色；Gemini 3.8 TTS "
                    "原生支持欧洲葡语 pt-PT。"
                ),
                "chirp_custom_encoding": "IPA",
            },
        ],
        "default_style": (
            "Confident, natural product presenter with crisp articulation."
        ),
    },
    {
        "id": "zh",
        "label": "Chinese (中文 · 普通话)",
        "label_zh": "中文（普通话 · cmn-CN）",
        "default_locale": "cmn-CN",
        "locales": [
            {
                "code": "cmn-CN",
                "label": "中文（普通话 · 简体）— cmn-CN",
                "label_zh": "中文（普通话 · 简体）— cmn-CN",
                "chirp_locale": "cmn-CN",
                "chirp_custom_encoding": "PINYIN",
            },
        ],
        "default_style": (
            "Clear, modern Mandarin product keynote narrator with steady pace."
        ),
    },
]

PREBUILT_VOICES: list[dict[str, str]] = [
    {
        "name": "Kore",
        "gender": "Female",
        "gender_zh": "女声",
        "character": "Firm, clear, flagship commercial narrator",
        "character_zh": "沉稳清晰 · 旗舰商业旁白",
    },
    {
        "name": "Puck",
        "gender": "Male",
        "gender_zh": "男声",
        "character": "Upbeat, energetic, modern presenter",
        "character_zh": "活力明快 · 现代产品主讲",
    },
    {
        "name": "Aoede",
        "gender": "Female",
        "gender_zh": "女声",
        "character": "Warm, breezy, conversational",
        "character_zh": "温和自然 · 亲切对话感",
    },
    {
        "name": "Charon",
        "gender": "Male",
        "gender_zh": "男声",
        "character": "Informative, authoritative, broadcast",
        "character_zh": "专业权威 · 新闻播报风",
    },
    {
        "name": "Leda",
        "gender": "Female",
        "gender_zh": "女声",
        "character": "Crisp, articulate, youthful",
        "character_zh": "清脆干练 · 年轻清晰",
    },
    {
        "name": "Zephyr",
        "gender": "Female",
        "gender_zh": "女声",
        "character": "Bright, friendly, assistant-grade",
        "character_zh": "明亮友好 · 智能车载助手",
    },
    {
        "name": "Fenrir",
        "gender": "Male",
        "gender_zh": "男声",
        "character": "Dynamic, expressive automotive launch",
        "character_zh": "动感张力 · 汽车发布会风",
    },
    {
        "name": "Orus",
        "gender": "Male",
        "gender_zh": "男声",
        "character": "Steady, technical, assured",
        "character_zh": "稳重可靠 · 科技解说",
    },
    {
        "name": "Sulafat",
        "gender": "Female",
        "gender_zh": "女声",
        "character": "Smooth, warm storytelling",
        "character_zh": "柔和顺滑 · 叙事播讲",
    },
    {
        "name": "Despina",
        "gender": "Female",
        "gender_zh": "女声",
        "character": "Polished, balanced studio tone",
        "character_zh": "均衡精致 · 录音棚质感",
    },
    {
        "name": "Achird",
        "gender": "Male",
        "gender_zh": "男声",
        "character": "Friendly, natural conversational",
        "character_zh": "随和自然 · 日常交流",
    },
    {
        "name": "Schedar",
        "gender": "Male",
        "gender_zh": "男声",
        "character": "Even, documentary clarity",
        "character_zh": "平实清晰 · 纪录片旁白",
    },
]

PRESET_SCRIPTS: dict[str, list[dict[str, str]]] = {
    "es": [
        {
            "id": "es_voltara_launch",
            "title": "Voltara EX2 Urban EV Launch (Spanish + English Brands)",
            "title_zh": "Voltara EX2 城市纯电发布（西语 + 英语品牌混读）",
            "text": (
                "Descubre el nuevo Voltara Ex2, el SUV eléctrico compacto "
                "diseñado para la ciudad. Con hasta 410 kilómetros de "
                "autonomía WLTP, conexión inalámbrica con Apple CarPlay y "
                "actualizaciones OTA inteligentes, el Voltara Ex2 redefine "
                "la movilidad urbana."
            ),
        },
        {
            "id": "es_smart_cockpit",
            "title": "Smart Cockpit, LiDAR & Cloud Telemetry",
            "title_zh": "智能座舱、LiDAR 感知与 SQL 云端遥测",
            "text": (
                "La arquitectura digital del Voltara EX2 integra sensores "
                "LiDAR de alta precisión y diagnóstico en tiempo real "
                "mediante SQL, elevando la seguridad de tu SUV en cada ruta."
            ),
        },
    ],
    "pt": [
        {
            "id": "pt_voltara_launch",
            "title": "Lançamento Voltara EX2 (Português + Marcas em Inglês)",
            "title_zh": "Voltara EX2 巴西/葡语发布（葡语 + 英语品牌混读）",
            "text": (
                "Conheça o novo Voltara Ex2, o SUV elétrico compacto feito "
                "para o seu dia a dia. Com até 410 quilômetros de autonomia "
                "WLTP, integração sem fio com Apple CarPlay e atualizações "
                "OTA inteligentes, o Voltara Ex2 transforma a mobilidade urbana."
            ),
        },
        {
            "id": "pt_smart_cockpit",
            "title": "Sensores LiDAR & Telemetria SQL",
            "title_zh": "LiDAR 激光雷达与 SQL 云端诊断",
            "text": (
                "A plataforma conectada do Voltara EX2 combina sensores LiDAR "
                "de última geração com análise em nuvem via SQL para "
                "proteger cada viagem no seu SUV."
            ),
        },
    ],
    "zh": [
        {
            "id": "zh_voltara_launch",
            "title": "Voltara EX2 Pure EV Launch (Mandarin + English Brands)",
            "title_zh": "Voltara EX2 纯电旗舰发布（中英混读 + 品牌与缩写）",
            "text": (
                "欢迎体验全新 Voltara Ex2 智能纯电 SUV，拥有高达 410 公里的 "
                "WLTP 续航表现，全面支持 Apple CarPlay 无线互联、LiDAR "
                "智能感知与 OTA 在线升级。"
            ),
        },
        {
            "id": "zh_cockpit_polyphone",
            "title": "Smart Cockpit & Polyphone Control (银行 / 行人 / SQL)",
            "title_zh": "智能座舱与多音字精准控制（银行 / 行人 / SQL）",
            "text": (
                "驾驶 Voltara EX2 经过银行路口时，LiDAR 会精准识别行人，并通过 "
                "SQL 云端遥测与 OTA 持续优化行车安全。"
            ),
        },
    ],
}

DEFAULT_GLOSSARY: list[dict[str, Any]] = [
    {
        "id": "voltara_ex2",
        "term": "Voltara EX2",
        "category": "brand_model",
        "enabled": True,
        "note": (
            "Headline brand + alphanumeric model code. Compare Standard English "
            "('Vol-tah-rah E-X two') vs. Native localized reading."
        ),
        "english": {
            "gemini": "Vol-tah-rah E-X two",
            "chirp_ipa_en": "vɒlˈtɑːrə ˈiː ˈɛks ˈtuː",
            "chirp_ipa_es": "bolˈta.ɾa ˈi.ˈeks.ˈtu",
            "chirp_ipa_pt": "vowˈta.ɾɐ ˈi.ˈɛks.ˈtu",
            "chirp_ssml": (
                '<phoneme alphabet="ipa" ph="vɒlˈtɑːrə">Voltara</phoneme> '
                '<say-as interpret-as="characters">EX</say-as> two'
            ),
        },
        "native": {
            "es": {
                "gemini": "Bol-ta-ra E equis dos",
                "chirp_ipa": "bolˈta.ɾa e.ˈe.kis.ˈdos",
                "chirp_ssml": (
                    '<phoneme alphabet="ipa" ph="bolˈta.ɾa">Voltara</phoneme> '
                    "E equis dos"
                ),
            },
            "pt": {
                "gemini": "Vol-tá-ra É xis dois",
                "chirp_ipa": "vowˈta.ɾɐ ˈɛ ˈʃis ˈdojs",
                "chirp_ssml": (
                    '<phoneme alphabet="ipa" ph="vowˈta.ɾɐ">Voltara</phoneme> '
                    "É xis dois"
                ),
            },
            "zh": {
                "gemini": "沃尔塔拉 E-X 二",
                "chirp_pinyin_phrase": "沃尔塔拉",
                "chirp_pinyin": "wo4 er3 ta3 la1",
                "chirp_text_sub": "沃尔塔拉 E X 二",
                "chirp_ssml": '<sub alias="沃尔塔拉 E X 二">Voltara EX2</sub>',
            },
        },
    },
    {
        "id": "voltara",
        "term": "Voltara",
        "category": "brand",
        "enabled": True,
        "note": "Standalone automotive brand name when not followed by EX2.",
        "english": {
            "gemini": "Vol-tah-rah",
            "chirp_ipa_en": "vɒlˈtɑːrə",
            "chirp_ipa_es": "bolˈta.ɾa",
            "chirp_ipa_pt": "vowˈta.ɾɐ",
            "chirp_ssml": '<phoneme alphabet="ipa" ph="vɒlˈtɑːrə">Voltara</phoneme>',
        },
        "native": {
            "es": {
                "gemini": "Bol-ta-ra",
                "chirp_ipa": "bolˈta.ɾa",
                "chirp_ssml": '<phoneme alphabet="ipa" ph="bolˈta.ɾa">Voltara</phoneme>',
            },
            "pt": {
                "gemini": "Vol-tá-ra",
                "chirp_ipa": "vowˈta.ɾɐ",
                "chirp_ssml": '<phoneme alphabet="ipa" ph="vowˈta.ɾɐ">Voltara</phoneme>',
            },
            "zh": {
                "gemini": "沃尔塔拉",
                "chirp_pinyin_phrase": "沃尔塔拉",
                "chirp_pinyin": "wo4 er3 ta3 la1",
                "chirp_text_sub": "沃尔塔拉",
                "chirp_ssml": '<sub alias="沃尔塔拉">Voltara</sub>',
            },
        },
    },
    {
        "id": "suv",
        "term": "SUV",
        "category": "acronym",
        "enabled": True,
        "note": "Automotive segment initialism (lettered in EN/ES/PT, localized in ZH).",
        "english": {
            "gemini": "S-U-V",
            "chirp_ipa_en": "ˌɛsjuːˈviː",
            "chirp_ipa_es": "es.ju.ˈbi",
            "chirp_ipa_pt": "ɛs.ju.ˈvi",
            "chirp_ssml": '<say-as interpret-as="characters">SUV</say-as>',
        },
        "native": {
            "es-ES": {
                "gemini": "ese u uve",
                "chirp_ipa": "ˈe.se.ˈu.ˈu.be",
                "chirp_ssml": '<sub alias="ese u uve">SUV</sub>',
            },
            "es-US": {
                "gemini": "ese u ve",
                "chirp_ipa": "ˈe.se.ˈu.ˈbe",
                "chirp_ssml": '<sub alias="ese u ve">SUV</sub>',
            },
            "es": {
                "gemini": "ese u uve",
                "chirp_ipa": "ˈe.se.ˈu.ˈu.be",
                "chirp_ssml": '<sub alias="ese u uve">SUV</sub>',
            },
            "pt": {
                "gemini": "ésse u vê",
                "chirp_ipa": "ˈɛ.si.ˈu.ˈve",
                "chirp_ssml": '<sub alias="ésse u vê">SUV</sub>',
            },
            "zh": {
                "gemini": "运动型多用途车",
                "chirp_pinyin_phrase": "运动型多用途车",
                "chirp_pinyin": "yun4 dong4 xing2 duo1 yong4 tu2 che1",
                "chirp_text_sub": "运动型多用途车",
                "chirp_ssml": '<sub alias="运动型多用途车">SUV</sub>',
            },
        },
    },
    {
        "id": "ota",
        "term": "OTA",
        "category": "acronym",
        "enabled": True,
        "note": "Over-The-Air firmware update initialism.",
        "english": {
            "gemini": "O-T-A",
            "chirp_ipa_en": "ˌoʊtiːˈeɪ",
            "chirp_ipa_es": "ow.ti.ˈej",
            "chirp_ipa_pt": "ow.ti.ˈej",
            "chirp_ssml": '<say-as interpret-as="characters">OTA</say-as>',
        },
        "native": {
            "es": {
                "gemini": "o te a",
                "chirp_ipa": "ˈo.te.ˈa",
                "chirp_ssml": '<sub alias="o te a">OTA</sub>',
            },
            "pt": {
                "gemini": "ó tê á",
                "chirp_ipa": "ˈɔ.ˈte.ˈa",
                "chirp_ssml": '<sub alias="ó tê á">OTA</sub>',
            },
            "zh": {
                "gemini": "远程无线升级",
                "chirp_pinyin_phrase": "远程无线升级",
                "chirp_pinyin": "yuan3 cheng2 wu2 xian4 sheng1 ji2",
                "chirp_text_sub": "远程无线升级",
                "chirp_ssml": '<sub alias="远程无线升级">OTA</sub>',
            },
        },
    },
    {
        "id": "wltp",
        "term": "WLTP",
        "category": "acronym",
        "enabled": True,
        "note": "Worldwide Harmonised Light Vehicles Test Procedure range standard.",
        "english": {
            "gemini": "W-L-T-P",
            "chirp_ipa_en": "ˈdʌbəljuː ˈɛl ˈtiː ˈpiː",
            "chirp_ipa_es": "ˈda.bel.ju.ˈel.ˈti.ˈpi",
            "chirp_ipa_pt": "ˈdɐ.bew.ju.ˈɛw.ˈti.ˈpi",
            "chirp_ssml": '<say-as interpret-as="characters">WLTP</say-as>',
        },
        "native": {
            "es-ES": {
                "gemini": "uve doble ele te pe",
                "chirp_ipa": "ˈu.be.ˈdo.ble.ˈe.le.ˈte.ˈpe",
                "chirp_ssml": '<sub alias="uve doble ele te pe">WLTP</sub>',
            },
            "es-US": {
                "gemini": "doble ve ele te pe",
                "chirp_ipa": "ˈdo.ble.ˈbe.ˈe.le.ˈte.ˈpe",
                "chirp_ssml": '<sub alias="doble ve ele te pe">WLTP</sub>',
            },
            "es": {
                "gemini": "uve doble ele te pe",
                "chirp_ipa": "ˈu.be.ˈdo.ble.ˈe.le.ˈte.ˈpe",
                "chirp_ssml": '<sub alias="uve doble ele te pe">WLTP</sub>',
            },
            "pt": {
                "gemini": "dáblio éle tê pê",
                "chirp_ipa": "ˈda.bliw.ˈɛ.li.ˈte.ˈpe",
                "chirp_ssml": '<sub alias="dáblio éle tê pê">WLTP</sub>',
            },
            "zh": {
                "gemini": "全球轻型车测试规程",
                "chirp_pinyin_phrase": "全球轻型车测试规程",
                "chirp_pinyin": "quan2 qiu2 qing1 xing2 che1 ce4 shi4 gui1 cheng2",
                "chirp_text_sub": "全球轻型车测试规程",
                "chirp_ssml": '<sub alias="全球轻型车测试规程">WLTP</sub>',
            },
        },
    },
    {
        "id": "apple_carplay",
        "term": "Apple CarPlay",
        "category": "brand",
        "enabled": True,
        "note": "Embedded English partner brand name inside multilingual copy.",
        "english": {
            "gemini": "Apple Car-Play",
            "chirp_ipa_en": "ˈæpəl ˈkɑːɹpleɪ",
            "chirp_ipa_es": "ˈa.pel ˈkaɾ.plej",
            "chirp_ipa_pt": "ˈɛ.pow ˈkaɾ ˈplej",
            "chirp_ssml": (
                '<phoneme alphabet="ipa" ph="ˈæpəl">Apple</phoneme> '
                '<phoneme alphabet="ipa" ph="ˈkɑːɹpleɪ">CarPlay</phoneme>'
            ),
        },
        "native": {
            "es": {
                "gemini": "Ápol Car Pley",
                "chirp_ipa": "ˈa.pol ˈkaɾ.plej",
                "chirp_ssml": '<sub alias="Ápol Car Pley">Apple CarPlay</sub>',
            },
            "pt": {
                "gemini": "Épol Car Plei",
                "chirp_ipa": "ˈɛ.pow ˈkaɾ ˈplej",
                "chirp_ssml": '<sub alias="Épol Car Plei">Apple CarPlay</sub>',
            },
            "zh": {
                "gemini": "苹果车载系统",
                "chirp_pinyin_phrase": "苹果车载系统",
                "chirp_pinyin": "ping2 guo3 che1 zai4 xi4 tong3",
                "chirp_text_sub": "苹果车载系统",
                "chirp_ssml": '<sub alias="苹果车载系统">Apple CarPlay</sub>',
            },
        },
    },
    {
        "id": "lidar",
        "term": "LiDAR",
        "category": "terminology",
        "enabled": True,
        "note": "Autonomous driving sensor terminology (/ˈlaɪdɑːɹ/ vs. /ˈli.daɾ/).",
        "english": {
            "gemini": "LYE-dar",
            "chirp_ipa_en": "ˈlaɪdɑːɹ",
            "chirp_ipa_es": "ˈlaj.daɾ",
            "chirp_ipa_pt": "ˈlaj.daɾ",
            "chirp_ssml": '<phoneme alphabet="ipa" ph="ˈlaɪdɑːɹ">LiDAR</phoneme>',
        },
        "native": {
            "es": {
                "gemini": "lídar",
                "chirp_ipa": "ˈli.daɾ",
                "chirp_ssml": '<phoneme alphabet="ipa" ph="ˈli.daɾ">LiDAR</phoneme>',
            },
            "pt": {
                "gemini": "lídar",
                "chirp_ipa": "ˈli.daɾ",
                "chirp_ssml": '<phoneme alphabet="ipa" ph="ˈli.daɾ">LiDAR</phoneme>',
            },
            "zh": {
                "gemini": "激光雷达",
                "chirp_pinyin_phrase": "激光雷达",
                "chirp_pinyin": "ji1 guang1 lei2 da2",
                "chirp_text_sub": "激光雷达",
                "chirp_ssml": '<sub alias="激光雷达">LiDAR</sub>',
            },
        },
    },
    {
        "id": "sql",
        "term": "SQL",
        "category": "acronym",
        "enabled": True,
        "note": "Database query language ('sequel' in EN vs. localized letter/term).",
        "english": {
            "gemini": "sequel",
            "chirp_ipa_en": "ˈsiːkwəl",
            "chirp_ipa_es": "ˈsi.kwel",
            "chirp_ipa_pt": "ˈsi.kwew",
            "chirp_ssml": '<phoneme alphabet="ipa" ph="ˈsiːkwəl">SQL</phoneme>',
        },
        "native": {
            "es": {
                "gemini": "ese cu ele",
                "chirp_ipa": "ˈe.se.ˈku.ˈe.le",
                "chirp_ssml": '<sub alias="ese cu ele">SQL</sub>',
            },
            "pt": {
                "gemini": "ésse quê éle",
                "chirp_ipa": "ˈɛ.si.ˈke.ˈɛ.li",
                "chirp_ssml": '<sub alias="ésse quê éle">SQL</sub>',
            },
            "zh": {
                "gemini": "结构化查询语言",
                "chirp_pinyin_phrase": "结构化查询语言",
                "chirp_pinyin": "jie2 gou4 hua4 cha2 xun2 yu3 yan2",
                "chirp_text_sub": "结构化查询语言",
                "chirp_ssml": '<sub alias="结构化查询语言">SQL</sub>',
            },
        },
    },
    {
        "id": "zh_yinhang",
        "term": "银行",
        "category": "terminology",
        "enabled": True,
        "note": "Mandarin polyphone showcase: 行 pronounced háng (bank) vs. xíng (pedestrian).",
        "english": {
            "gemini": "银行",
            "chirp_ssml": "银行",
        },
        "native": {
            "zh": {
                "gemini": "银杭",
                "chirp_pinyin_phrase": "银行",
                "chirp_pinyin": "yin2 hang2",
                "chirp_text_sub": "银行",
                "chirp_ssml": "银行",
            },
        },
    },
]
