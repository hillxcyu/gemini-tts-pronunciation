/**
 * Copyright 2026 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * Interactive Multilingual & Custom Terminology Pronunciation Studio client.
 * Supports instant EN / CN (Simplified Chinese) UI localization and uses
 * standard locale-aware Intl formatters for all numerical & unit UI displays.
 */

const UI_STRINGS = {
  en: {
    docTitle:
      "Multilingual & Custom Terminology Pronunciation Studio — Gemini 3.8 TTS & Chirp 3 HD",
    headerTitle: "Multilingual & Custom Terminology Pronunciation Studio",
    headerSubtitle:
      "Gemini 3.8 TTS (Vertex AI Global · Dual-Track Normalization & Native Code-Switching) & Chirp 3 HD (Cloud TTS · IPA / Pinyin & SSML Phonetics)",
    uiLangLabel: "UI",
    ctrlMainLang: "1. Main Language",
    ctrlRegionalLocale: "Regional Locale",
    ctrlPronMode: "2. Brand, Terminology & Acronym Pronunciation",
    modeEnglish: "Standard English",
    modeNative: "Native Language",
    modeRaw: "Raw (Uncontrolled)",
    ctrlVoicePersona: "3. Prebuilt Voice Persona",
    ctrlSynthesisMode: "4. Synthesis Mode",
    engineCompare: "Compare Both (Gemini 3.8 + Chirp 3 HD)",
    engineGeminiOnly: "Gemini 3.8 TTS Only",
    engineChirpOnly: "Chirp 3 HD Only",
    scriptPanelTitle: "Multilingual Script & Phonetic Compiler",
    scriptPanelCaptionHtml:
      "Edit code-switched copy or select a preset featuring <strong>Voltara EX2</strong> and technical acronyms.",
    presetLabel: "Sample Preset",
    displayTextLabel: "Display Text (UI / Subtitle Track)",
    detectedTermsLabel: "Detected Custom Terms & Brand Spans",
    geminiParamsTitle: "Gemini 3.8 TTS Parameters",
    modelTierLabel: "Model Tier",
    styleFieldLabelHtml: "Turn Delivery Style (<code>speechMetadata.style</code>)",
    stylePlaceholder: "Warm, polished automotive narrator...",
    insertPausesLabelHtml:
      "Insert micro-pause tags before custom terms (<code>&lt;short pause&gt;</code> / <code>&lt;break&gt;</code>)",
    chirpParamsTitle: "Chirp 3 HD Phonetic Controls",
    chirpMechanismLabel: "Phonetic Override Mechanism",
    chirpOptSsml: "SSML (<phoneme ipa> + <say-as> + <voice> Switch)",
    chirpOptCustomPron: "CustomPronunciations API (IPA / X-SAMPA / Pinyin Lexicon)",
    speakingRateLabel: "Chirp 3 HD Speaking Rate",
    chirpHelperNoteHtml:
      "Chirp 3 HD supports deterministic IPA (<code>es-*</code>, <code>pt-BR</code>), tone-numbered Pinyin (<code>cmn-CN</code>), and mid-sentence <code>&lt;voice&gt;</code> switching.",
    synthesizeBtn: "Synthesize & Compare Audio",
    statusSynthesizing: "Synthesizing audio via Google Cloud ADC…",
    statusComplete: "Synthesis complete.",
    statusFailed: "Synthesis failed.",
    geminiCompiledTitleHtml: "Normalized <code>parts[].text</code> Transcript",
    chirpCompiledSsml: (voice) => `Compiled SSML (${voice})`,
    chirpCompiledCustomPron: (voice) => `CustomPronunciations (${voice})`,
    chirpCompiledRaw: (voice) => `Raw Plaintext (${voice})`,
    audioPanelTitle: "Synthesized Audio Comparison",
    audioPanelCaptionHtml:
      "Listen to how each engine renders <strong>Voltara EX2</strong>, partner brands, and technical acronyms under the selected pronunciation mode.",
    geminiBadge: "Vertex AI · Global",
    geminiDefaultHeading: "Gemini 3.8 Flash TTS",
    geminiResultHeading: (model, voice) => `${model} · Voice: ${voice}`,
    geminiCardMeta:
      "Dual-track pre-TTS normalization + native multimodal code-switching",
    geminiEmptyPlayer:
      "Click “Synthesize & Compare Audio” to generate Gemini 3.8 TTS audio.",
    geminiPayloadSummaryHtml:
      "Inspect Vertex AI <code>generateContent</code> Request Payload",
    chirpBadge: "Cloud Text-to-Speech",
    chirpDefaultHeading: "Chirp 3 HD",
    chirpResultHeading: (voice, modeLabel) => `${voice} (${modeLabel})`,
    chirpModeBadgeSsml: "SSML",
    chirpModeBadgeCustom: "CustomPronunciations",
    chirpModeBadgeRaw: "Plaintext",
    chirpCardMeta:
      "Deterministic IPA / Pinyin phonemes & synchronous SSML control",
    chirpEmptyPlayer:
      "Click “Synthesize & Compare Audio” to generate Chirp 3 HD audio.",
    chirpPayloadSummaryHtml:
      "Inspect Cloud TTS <code>text:synthesize</code> Request Payload",
    downloadWav: "Download WAV",
    archTitle: "When to Use Gemini 3.8 TTS vs. Chirp 3 HD",
    archBulletGeminiHtml:
      "<strong>Gemini 3.8 TTS (<code>gemini-3.8-flash-tts</code> / <code>lite</code>):</strong> Best for seamless intra-sentence code-switching across 130 languages, expressive acting via <code>speechMetadata.style</code>, inline vocal pauses (<code>&lt;short pause&gt;</code>), and continuous speaker prosody using dual-track respelling.",
    archBulletChirpHtml:
      "<strong>Chirp 3 HD (<code>&lt;locale&gt;-Chirp3-HD-&lt;Voice&gt;</code>):</strong> Best when strict phoneme-level governance is required via <code>CustomPronunciations</code> (Greco IPA / X-SAMPA for <code>es-*</code> &amp; <code>pt-BR</code>; tone-numbered Pinyin for <code>cmn-CN</code>) or SSML <code>&lt;phoneme&gt;</code>, <code>&lt;say-as&gt;</code>, and <code>&lt;voice&gt;</code> tags.",
    glossaryPanelTitle: "Custom Terminology, Brand & Acronym Lexicon",
    glossaryCaptionHtml: (langCode) =>
      `Edit any rule live to adjust how Gemini 3.8 TTS respells or how Chirp 3 HD applies IPA / Pinyin / SSML overrides in the active language (<strong>${langCode}</strong>).`,
    addTermBtn: "+ Add Custom Term",
    resetGlossaryBtn: "Reset Defaults",
    thActive: "Active",
    thTerm: "Term / Acronym",
    thType: "Type",
    thEngGemini: "Standard English (Gemini Respelling)",
    thEngChirp: "Standard English (Chirp IPA / SSML)",
    thNatGemini: "Native Language (Gemini Respelling)",
    thNatChirp: "Native Language (Chirp IPA / Pinyin)",
    thActions: "Actions",
    catBrandModel: "Brand + Model",
    catBrand: "Brand",
    catAcronym: "Acronym",
    catTerminology: "Terminology",
    phEngChirp: "IPA (e.g. vɒlˈtɑːrə)",
    phNatPinyin: "Pinyin (e.g. wo4 er3 ta3 la1)",
    phNatIpa: "Greco IPA (e.g. bolˈta.ɾa)",
    removeBtn: "Remove",
    matchCountOne: "1 custom term active in script",
    matchCountOther: (numStr) => `${numStr} custom terms active in script`,
    termTooltip: (gem, chirp) => `Gemini: ${gem} | Chirp: ${chirp}`,
    iapSessionExpired:
      "IAP authentication session expired. Please refresh this page to re-authenticate.",
  },
  "zh-CN": {
    docTitle:
      "多语种与自定义专业术语发音工作台 — Gemini 3.8 TTS 与 Chirp 3 HD",
    headerTitle: "多语种与自定义专业术语发音工作台",
    headerSubtitle:
      "Gemini 3.8 TTS（Vertex AI 全球端点 · 双轨文本改写与原生混读）与 Chirp 3 HD（Cloud TTS · IPA / 拼音词典与 SSML 音素精控）",
    uiLangLabel: "界面语言",
    ctrlMainLang: "1. 主要合成语种",
    ctrlRegionalLocale: "区域口音 (Locale)",
    ctrlPronMode: "2. 品牌、专业术语与缩写发音模式",
    modeEnglish: "标准英语发音",
    modeNative: "母语本土化发音",
    modeRaw: "原始未控基线",
    ctrlVoicePersona: "3. 预置音色选择",
    ctrlSynthesisMode: "4. 合成对比模式",
    engineCompare: "双引擎并排对比 (Gemini 3.8 + Chirp 3 HD)",
    engineGeminiOnly: "仅 Gemini 3.8 TTS",
    engineChirpOnly: "仅 Chirp 3 HD",
    scriptPanelTitle: "多语种混读文稿与音素编译器",
    scriptPanelCaptionHtml:
      "可直接编辑跨语种混读文本，或选择内置的 <strong>Voltara EX2</strong> 及汽车科技缩写示例。",
    presetLabel: "预设示例文稿",
    displayTextLabel: "展示文本（前端字幕 / 原始显示轨道）",
    detectedTermsLabel: "已识别的自定义品牌、缩写与专业术语",
    geminiParamsTitle: "Gemini 3.8 TTS 参数配置",
    modelTierLabel: "模型规格",
    styleFieldLabelHtml: "演播风格提示词 (<code>speechMetadata.style</code>)",
    stylePlaceholder: "例如：Warm, polished automotive narrator...",
    insertPausesLabelHtml:
      "在自定义术语前插入微停顿标签 (<code>&lt;short pause&gt;</code> / <code>&lt;break&gt;</code>)",
    chirpParamsTitle: "Chirp 3 HD 精细音素控制",
    chirpMechanismLabel: "音素干预机制",
    chirpOptSsml: "SSML 标签 (<phoneme> 音素 + <say-as> + <voice> 同音色跨语种切换)",
    chirpOptCustomPron: "CustomPronunciations 词典 API (IPA / X-SAMPA / 拼音声调)",
    speakingRateLabel: "Chirp 3 HD 语速倍率",
    chirpHelperNoteHtml:
      "Chirp 3 HD 支持确定性音素词典（<code>es-*</code>、<code>pt-BR</code> 使用 IPA，<code>cmn-CN</code> 使用带数字声调拼音）及句内 <code>&lt;voice&gt;</code> 切换。",
    synthesizeBtn: "立即合成并对比音频",
    statusSynthesizing: "正在通过 Google Cloud ADC 合成音频…",
    statusComplete: "音频合成完成。",
    statusFailed: "音频合成失败。",
    geminiCompiledTitleHtml: "归一化后 <code>parts[].text</code> 合成文本",
    chirpCompiledSsml: (voice) => `编译后 SSML (${voice})`,
    chirpCompiledCustomPron: (voice) => `编译后 CustomPronunciations 词典 (${voice})`,
    chirpCompiledRaw: (voice) => `原始纯文本 (${voice})`,
    audioPanelTitle: "双引擎合成音频并排对比",
    audioPanelCaptionHtml:
      "对比试听双引擎在当前发音模式下对 <strong>Voltara EX2</strong>、合作品牌及专业缩写的实际发音表现。",
    geminiBadge: "Vertex AI · 全球端点",
    geminiDefaultHeading: "Gemini 3.8 Flash TTS",
    geminiResultHeading: (model, voice) => `${model} · 音色：${voice}`,
    geminiCardMeta: "双轨前置文本归一化 + 多模态句内无缝语码转换",
    geminiEmptyPlayer: "点击左侧「立即合成并对比音频」生成 Gemini 3.8 TTS 语音。",
    geminiPayloadSummaryHtml:
      "查看 Vertex AI <code>generateContent</code> 原始请求 JSON",
    chirpBadge: "Cloud Text-to-Speech 语音服务",
    chirpDefaultHeading: "Chirp 3 HD",
    chirpResultHeading: (voice, modeLabel) => `${voice}（${modeLabel}）`,
    chirpModeBadgeSsml: "SSML 音素控制",
    chirpModeBadgeCustom: "CustomPronunciations 词典",
    chirpModeBadgeRaw: "原始纯文本",
    chirpCardMeta: "确定性 IPA / 拼音音素词典与同步 SSML 精细控制",
    chirpEmptyPlayer: "点击左侧「立即合成并对比音频」生成 Chirp 3 HD 语音。",
    chirpPayloadSummaryHtml:
      "查看 Cloud TTS <code>text:synthesize</code> 原始请求 JSON",
    downloadWav: "下载 WAV",
    archTitle: "Gemini 3.8 TTS 与 Chirp 3 HD 选型建议",
    archBulletGeminiHtml:
      "<strong>Gemini 3.8 TTS (<code>gemini-3.8-flash-tts</code> / <code>lite</code>)：</strong>适用于覆盖 130 种语言的句内自然中英/西英混读、通过 <code>speechMetadata.style</code> 控制情感表现力、内联停顿标签 (<code>&lt;short pause&gt;</code>) 以及保持跨语种音色连贯性（配合双轨注音改写）。",
    archBulletChirpHtml:
      "<strong>Chirp 3 HD (<code>&lt;locale&gt;-Chirp3-HD-&lt;Voice&gt;</code>)：</strong>适用于需要严格音素级发音治理的场景，支持通过 <code>CustomPronunciations</code>（<code>es-*</code> 与 <code>pt-BR</code> 支持 Greco IPA / X-SAMPA，<code>cmn-CN</code> 强制使用带声调拼音）或 SSML <code>&lt;phoneme&gt;</code>、<code>&lt;say-as&gt;</code> 与 <code>&lt;voice&gt;</code> 精准锁定读音。",
    glossaryPanelTitle: "自定义专业术语、品牌与缩写发音词表",
    glossaryCaptionHtml: (langCode) =>
      `实时编辑词表规则，调整当前激活语种 (<strong>${langCode}</strong>) 下 Gemini 3.8 TTS 的拼写改写与 Chirp 3 HD 的 IPA / 拼音 / SSML 音素映射。`,
    addTermBtn: "+ 新增自定义术语",
    resetGlossaryBtn: "恢复默认词表",
    thActive: "启用",
    thTerm: "术语 / 品牌 / 缩写",
    thType: "类别",
    thEngGemini: "标准英语发音 (Gemini 改写)",
    thEngChirp: "标准英语发音 (Chirp IPA / SSML)",
    thNatGemini: "母语本土化发音 (Gemini 改写)",
    thNatChirp: "母语本土化音素 (Chirp IPA / 拼音)",
    thActions: "操作",
    catBrandModel: "品牌 + 车型",
    catBrand: "品牌名称",
    catAcronym: "字母缩写",
    catTerminology: "专业术语 / 多音字",
    phEngChirp: "英语 IPA（如 ˈdʒiːli）",
    phNatPinyin: "带声调拼音（如 ji2 li4）",
    phNatIpa: "Greco 音素 IPA（如 ˈji.li）",
    removeBtn: "移除",
    matchCountOne: "当前文稿命中 1 处自定义术语",
    matchCountOther: (numStr) => `当前文稿命中 ${numStr} 处自定义术语`,
    termTooltip: (gem, chirp) => `Gemini 改写：${gem} | Chirp 音素：${chirp}`,
    iapSessionExpired: "Google IAP 登录会话已过期，请刷新当前页面重新完成身份验证。",
  },
};

const state = {
  uiLang: localStorage.getItem("tts_studio_ui_lang") === "zh-CN" ? "zh-CN" : "en",
  config: null,
  activeLangId: "es",
  languageCode: "es-ES",
  pronunciationMode: "english",
  voiceName: "Kore",
  engine: "compare",
  geminiModel: "gemini-3.8-flash-tts",
  chirpControlMode: "ssml",
  speakingRate: 1.0,
  insertPauses: false,
  glossary: [],
  previewTimer: null,
  lastCompiled: null,
  lastResults: {},
  statusKey: null,
};

function t(key) {
  const dict = UI_STRINGS[state.uiLang] || UI_STRINGS.en;
  return dict[key] !== undefined ? dict[key] : UI_STRINGS.en[key];
}

function getUiFormatLocale() {
  return state.uiLang === "zh-CN" ? "zh-CN" : "en-US";
}

// Locale-aware standard Intl formatters
function formatLatencyMs(ms) {
  const loc = getUiFormatLocale();
  try {
    return new Intl.NumberFormat(loc, {
      style: "unit",
      unit: "millisecond",
      unitDisplay: "short",
      maximumFractionDigits: 0,
    }).format(ms);
  } catch {
    return new Intl.NumberFormat(loc, { maximumFractionDigits: 0 }).format(ms);
  }
}

function formatDurationSec(seconds) {
  const loc = getUiFormatLocale();
  try {
    return new Intl.NumberFormat(loc, {
      style: "unit",
      unit: "second",
      unitDisplay: "short",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(seconds);
  } catch {
    return new Intl.NumberFormat(loc, { maximumFractionDigits: 2 }).format(seconds);
  }
}

function formatRateMultiplier(rate) {
  const loc = getUiFormatLocale();
  const formatted = new Intl.NumberFormat(loc, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(rate);
  return `${formatted}×`;
}

function formatMatchCount(count) {
  if (state.uiLang !== "zh-CN" && count === 1) {
    return t("matchCountOne");
  }
  const numStr = new Intl.NumberFormat(getUiFormatLocale()).format(count);
  return t("matchCountOther")(numStr);
}

function cloneDeep(obj) {
  return JSON.parse(JSON.stringify(obj));
}

async function parseJsonSafe(resp) {
  if (resp.redirected && resp.url && resp.url.includes("accounts.google.com")) {
    throw new Error(t("iapSessionExpired"));
  }
  const contentType = (resp.headers.get("content-type") || "").toLowerCase();
  if (!contentType.includes("application/json")) {
    const rawText = await resp.text();
    if (rawText.includes("accounts.google.com") || resp.status === 401) {
      throw new Error(t("iapSessionExpired"));
    }
    const titleMatch = rawText.match(/<title[^>]*>([^<]+)<\/title>/i);
    const summary = titleMatch ? titleMatch[1].trim() : `HTTP ${resp.status}`;
    throw new Error(summary);
  }
  return resp.json();
}

async function initApp() {
  const resp = await fetch("/api/config", { credentials: "same-origin" });
  const config = await parseJsonSafe(resp);
  state.config = config;
  state.glossary = cloneDeep(config.default_glossary || []);

  if (config.gcp) {
    document.getElementById("gcp-config-name").textContent = config.gcp.gcloud_config;
    document.getElementById("gcp-project-id").textContent = config.gcp.project_id;
    document.getElementById("gcp-location").textContent = config.gcp.location;
  }

  applyUiLanguage(state.uiLang, true);
  bindEvents();
}

function applyUiLanguage(uiLang, isInitial = false) {
  state.uiLang = uiLang === "zh-CN" ? "zh-CN" : "en";
  localStorage.setItem("tts_studio_ui_lang", state.uiLang);
  document.documentElement.lang = state.uiLang;
  document.title = t("docTitle");

  // Update EN / CN toggle buttons
  document.querySelectorAll("#ui-lang-switcher .seg-btn").forEach((btn) => {
    const active = btn.dataset.uiLang === state.uiLang;
    btn.classList.toggle("active", active);
    btn.setAttribute("aria-pressed", active ? "true" : "false");
  });

  // Translate all static data-i18n and data-i18n-html nodes
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    // Avoid overwriting empty-player container if audio is already rendered inside
    if (
      (key === "geminiEmptyPlayer" && state.lastResults.gemini) ||
      (key === "chirpEmptyPlayer" && state.lastResults.chirp3_hd)
    ) {
      return;
    }
    const val = t(key);
    if (typeof val === "string") {
      el.textContent = val;
    }
  });

  document.querySelectorAll("[data-i18n-html]").forEach((el) => {
    const key = el.getAttribute("data-i18n-html");
    const val = t(key);
    if (typeof val === "string") {
      el.innerHTML = val;
    }
  });

  document.getElementById("gemini-style-input").placeholder = t("stylePlaceholder");

  renderLanguageTabs();
  renderVoiceOptions();
  renderGeminiModelOptions();

  if (isInitial) {
    syncLanguageSelection("es", true);
  } else {
    refreshLocaleAndPresetLabels();
    updateGlossaryCaption();
    document.getElementById("speaking-rate-value").textContent = formatRateMultiplier(
      state.speakingRate
    );
    renderGlossaryTable();

    if (state.statusKey) {
      document.getElementById("synthesis-status").textContent = t(state.statusKey);
    }
    if (state.lastCompiled) {
      renderCompiledPreview(state.lastCompiled);
    }
    if (!state.lastResults.gemini) {
      document.getElementById("gemini-card-heading").textContent = t("geminiDefaultHeading");
    } else {
      renderAudioResult("gemini", state.lastResults.gemini, false);
    }
    if (!state.lastResults.chirp3_hd) {
      document.getElementById("chirp-card-heading").textContent = t("chirpDefaultHeading");
    } else {
      renderAudioResult("chirp", state.lastResults.chirp3_hd, false);
    }
  }
}

function renderLanguageTabs() {
  if (!state.config) return;
  const container = document.getElementById("language-tabs");
  container.innerHTML = "";
  const isZhUi = state.uiLang === "zh-CN";
  for (const lang of state.config.languages) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.id = `lang-tab-${lang.id}`;
    btn.className = `seg-btn${lang.id === state.activeLangId ? " active" : ""}`;
    btn.textContent = isZhUi && lang.label_zh ? lang.label_zh : lang.label;
    btn.setAttribute("role", "tab");
    btn.setAttribute("aria-selected", lang.id === state.activeLangId ? "true" : "false");
    btn.addEventListener("click", () => syncLanguageSelection(lang.id, true));
    container.appendChild(btn);
  }
}

function renderVoiceOptions() {
  if (!state.config) return;
  const select = document.getElementById("voice-select");
  const currentVal = state.voiceName;
  select.innerHTML = "";
  const isZhUi = state.uiLang === "zh-CN";
  for (const v of state.config.voices) {
    const opt = document.createElement("option");
    opt.value = v.name;
    const gender = isZhUi && v.gender_zh ? v.gender_zh : v.gender;
    const character = isZhUi && v.character_zh ? v.character_zh : v.character;
    opt.textContent = `${v.name} (${gender}) — ${character}`;
    if (v.name === currentVal) opt.selected = true;
    select.appendChild(opt);
  }
}

function renderGeminiModelOptions() {
  if (!state.config) return;
  const select = document.getElementById("gemini-model-select");
  const currentVal = state.geminiModel;
  select.innerHTML = "";
  const isZhUi = state.uiLang === "zh-CN";
  for (const m of state.config.gemini_models) {
    const opt = document.createElement("option");
    opt.value = m.id;
    opt.textContent = isZhUi && m.label_zh ? m.label_zh : m.label;
    if (m.id === currentVal) opt.selected = true;
    select.appendChild(opt);
  }
}

function refreshLocaleAndPresetLabels() {
  if (!state.config) return;
  const isZhUi = state.uiLang === "zh-CN";
  const langObj =
    state.config.languages.find((l) => l.id === state.activeLangId) || state.config.languages[0];

  const localeSelect = document.getElementById("locale-select");
  const prevLocale = state.languageCode;
  localeSelect.innerHTML = "";
  for (const loc of langObj.locales) {
    const opt = document.createElement("option");
    opt.value = loc.code;
    opt.textContent = isZhUi && loc.label_zh ? loc.label_zh : loc.label;
    if (loc.code === prevLocale) opt.selected = true;
    localeSelect.appendChild(opt);
  }

  const presetSelect = document.getElementById("preset-select");
  const prevPreset = presetSelect.value;
  presetSelect.innerHTML = "";
  const presets = state.config.presets[state.activeLangId] || [];
  presets.forEach((p, idx) => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = isZhUi && p.title_zh ? p.title_zh : p.title;
    if (prevPreset ? p.id === prevPreset : idx === 0) opt.selected = true;
    presetSelect.appendChild(opt);
  });
}

function updateGlossaryCaption() {
  const el = document.getElementById("glossary-panel-caption");
  if (el) {
    el.innerHTML = t("glossaryCaptionHtml")(state.languageCode);
  }
}

function syncLanguageSelection(langId, loadDefaultPreset = false) {
  state.activeLangId = langId;
  const langObj =
    state.config.languages.find((l) => l.id === langId) || state.config.languages[0];

  document.querySelectorAll("#language-tabs .seg-btn").forEach((btn) => {
    const active = btn.id === `lang-tab-${langId}`;
    btn.classList.toggle("active", active);
    btn.setAttribute("aria-selected", active ? "true" : "false");
  });

  state.languageCode = langObj.default_locale;
  document.getElementById("gemini-style-input").value = langObj.default_style || "";

  refreshLocaleAndPresetLabels();

  const presets = state.config.presets[langId] || [];
  if (loadDefaultPreset && presets.length > 0) {
    document.getElementById("preset-select").value = presets[0].id;
    document.getElementById("script-textarea").value = presets[0].text;
  }

  updateGlossaryCaption();
  document.getElementById("speaking-rate-value").textContent = formatRateMultiplier(
    state.speakingRate
  );

  renderGlossaryTable();
  schedulePreview();
}

function getNativeRuleRef(entry) {
  if (!entry.native) entry.native = {};
  const code = state.languageCode;
  const fam = state.activeLangId;
  if (entry.native[code]) return entry.native[code];
  if (!entry.native[fam]) {
    entry.native[fam] =
      fam === "zh"
        ? {
            gemini: entry.term,
            chirp_pinyin_phrase: entry.term,
            chirp_pinyin: "",
            chirp_text_sub: entry.term,
          }
        : { gemini: entry.term, chirp_ipa: "" };
  }
  return entry.native[fam];
}

function renderGlossaryTable() {
  const tbody = document.getElementById("glossary-tbody");
  tbody.innerHTML = "";
  const isZhTarget = state.activeLangId === "zh";

  state.glossary.forEach((entry, idx) => {
    const tr = document.createElement("tr");
    const eng = entry.english || (entry.english = { gemini: entry.term });
    const nat = getNativeRuleRef(entry);

    // 1. Enabled checkbox
    const tdEnabled = document.createElement("td");
    const chk = document.createElement("input");
    chk.type = "checkbox";
    chk.id = `glossary-enabled-${idx}`;
    chk.checked = entry.enabled !== false;
    chk.addEventListener("change", () => {
      entry.enabled = chk.checked;
      schedulePreview();
    });
    tdEnabled.appendChild(chk);

    // 2. Term
    const tdTerm = document.createElement("td");
    const inpTerm = document.createElement("input");
    inpTerm.type = "text";
    inpTerm.id = `glossary-term-${idx}`;
    inpTerm.className = "table-input";
    inpTerm.value = entry.term || "";
    inpTerm.addEventListener("input", () => {
      entry.term = inpTerm.value;
      schedulePreview();
    });
    tdTerm.appendChild(inpTerm);

    // 3. Category select
    const tdCat = document.createElement("td");
    const selCat = document.createElement("select");
    selCat.id = `glossary-cat-${idx}`;
    selCat.className = "table-input";
    [
      ["brand_model", t("catBrandModel")],
      ["brand", t("catBrand")],
      ["acronym", t("catAcronym")],
      ["terminology", t("catTerminology")],
    ].forEach(([val, label]) => {
      const o = document.createElement("option");
      o.value = val;
      o.textContent = label;
      if ((entry.category || "terminology") === val) o.selected = true;
      selCat.appendChild(o);
    });
    selCat.addEventListener("change", () => {
      entry.category = selCat.value;
      schedulePreview();
    });
    tdCat.appendChild(selCat);

    // 4. English Gemini Respelling
    const tdEngGem = document.createElement("td");
    const inpEngGem = document.createElement("input");
    inpEngGem.type = "text";
    inpEngGem.id = `glossary-eng-gem-${idx}`;
    inpEngGem.className = "table-input";
    inpEngGem.value = eng.gemini || "";
    inpEngGem.addEventListener("input", () => {
      eng.gemini = inpEngGem.value;
      schedulePreview();
    });
    tdEngGem.appendChild(inpEngGem);

    // 5. English Chirp IPA / SSML
    const tdEngChirp = document.createElement("td");
    const inpEngChirp = document.createElement("input");
    inpEngChirp.type = "text";
    inpEngChirp.id = `glossary-eng-chirp-${idx}`;
    inpEngChirp.className = "table-input mono";
    inpEngChirp.placeholder = t("phEngChirp");
    inpEngChirp.value = eng.chirp_ipa_en || eng.chirp_ssml || "";
    inpEngChirp.addEventListener("input", () => {
      const val = inpEngChirp.value.trim();
      if (val.startsWith("<")) {
        eng.chirp_ssml = val;
      } else {
        eng.chirp_ipa_en = val;
        delete eng.chirp_ssml;
      }
      schedulePreview();
    });
    tdEngChirp.appendChild(inpEngChirp);

    // 6. Native Gemini Respelling
    const tdNatGem = document.createElement("td");
    const inpNatGem = document.createElement("input");
    inpNatGem.type = "text";
    inpNatGem.id = `glossary-nat-gem-${idx}`;
    inpNatGem.className = "table-input";
    inpNatGem.value = nat.gemini || "";
    inpNatGem.addEventListener("input", () => {
      nat.gemini = inpNatGem.value;
      if (isZhTarget) {
        nat.chirp_text_sub = inpNatGem.value;
        delete nat.chirp_ssml;
      }
      schedulePreview();
    });
    tdNatGem.appendChild(inpNatGem);

    // 7. Native Chirp IPA / Pinyin
    const tdNatChirp = document.createElement("td");
    const inpNatChirp = document.createElement("input");
    inpNatChirp.type = "text";
    inpNatChirp.id = `glossary-nat-chirp-${idx}`;
    inpNatChirp.className = "table-input mono";
    inpNatChirp.placeholder = isZhTarget ? t("phNatPinyin") : t("phNatIpa");
    inpNatChirp.value = isZhTarget ? nat.chirp_pinyin || "" : nat.chirp_ipa || "";
    inpNatChirp.addEventListener("input", () => {
      if (isZhTarget) {
        nat.chirp_pinyin = inpNatChirp.value.trim();
        if (!nat.chirp_pinyin_phrase) {
          nat.chirp_pinyin_phrase = nat.chirp_text_sub || nat.gemini || entry.term;
        }
      } else {
        nat.chirp_ipa = inpNatChirp.value.trim();
        delete nat.chirp_ssml;
      }
      schedulePreview();
    });
    tdNatChirp.appendChild(inpNatChirp);

    // 8. Delete button
    const tdDel = document.createElement("td");
    const delBtn = document.createElement("button");
    delBtn.type = "button";
    delBtn.id = `glossary-del-${idx}`;
    delBtn.className = "delete-row-btn";
    delBtn.textContent = t("removeBtn");
    delBtn.addEventListener("click", () => {
      state.glossary.splice(idx, 1);
      renderGlossaryTable();
      schedulePreview();
    });
    tdDel.appendChild(delBtn);

    tr.append(tdEnabled, tdTerm, tdCat, tdEngGem, tdEngChirp, tdNatGem, tdNatChirp, tdDel);
    tbody.appendChild(tr);
  });
}

function bindEvents() {
  document.querySelectorAll("#ui-lang-switcher .seg-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      applyUiLanguage(btn.dataset.uiLang, false);
    });
  });

  document.getElementById("locale-select").addEventListener("change", (e) => {
    state.languageCode = e.target.value;
    updateGlossaryCaption();
    renderGlossaryTable();
    schedulePreview();
  });

  document.querySelectorAll("#pronunciation-mode-tabs .seg-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.pronunciationMode = btn.dataset.mode;
      document.querySelectorAll("#pronunciation-mode-tabs .seg-btn").forEach((b) => {
        const isActive = b === btn;
        b.classList.toggle("active", isActive);
        b.setAttribute("aria-checked", isActive ? "true" : "false");
      });
      schedulePreview();
    });
  });

  document.getElementById("voice-select").addEventListener("change", (e) => {
    state.voiceName = e.target.value;
    schedulePreview();
  });

  document.getElementById("engine-select").addEventListener("change", (e) => {
    state.engine = e.target.value;
    updateVisibleCards();
  });

  document.getElementById("preset-select").addEventListener("change", (e) => {
    const presets = state.config.presets[state.activeLangId] || [];
    const found = presets.find((p) => p.id === e.target.value);
    if (found) {
      document.getElementById("script-textarea").value = found.text;
      schedulePreview();
    }
  });

  document.getElementById("script-textarea").addEventListener("input", () => {
    schedulePreview();
  });

  document.getElementById("gemini-model-select").addEventListener("change", (e) => {
    state.geminiModel = e.target.value;
  });

  document.getElementById("chirp-mode-select").addEventListener("change", (e) => {
    state.chirpControlMode = e.target.value;
    schedulePreview();
  });

  document.getElementById("insert-pauses-checkbox").addEventListener("change", (e) => {
    state.insertPauses = e.target.checked;
    schedulePreview();
  });

  document.getElementById("speaking-rate-range").addEventListener("input", (e) => {
    state.speakingRate = parseFloat(e.target.value);
    document.getElementById("speaking-rate-value").textContent = formatRateMultiplier(
      state.speakingRate
    );
  });

  document.getElementById("add-term-btn").addEventListener("click", () => {
    state.glossary.unshift({
      id: `custom_${Date.now()}`,
      term: "BYD",
      category: "brand",
      enabled: true,
      english: {
        gemini: "B-Y-D",
        chirp_ssml: '<say-as interpret-as="characters">BYD</say-as>',
        chirp_ipa_es: "ˈbi.waj.ˈdi",
        chirp_ipa_pt: "ˈbi.waj.ˈdʒi",
      },
      native: {
        es: { gemini: "be i griega de", chirp_ipa: "ˈbe.i.ˈɡɾje.ɡa.ˈde" },
        pt: { gemini: "bê ípsilon dê", chirp_ipa: "ˈbe.ˈi.psi.lõ.ˈde" },
        zh: {
          gemini: "比亚迪",
          chirp_pinyin_phrase: "比亚迪",
          chirp_pinyin: "bi3 ya4 di2",
          chirp_text_sub: "比亚迪",
        },
      },
    });
    renderGlossaryTable();
    schedulePreview();
  });

  document.getElementById("reset-glossary-btn").addEventListener("click", () => {
    state.glossary = cloneDeep(state.config.default_glossary || []);
    renderGlossaryTable();
    schedulePreview();
  });

  document.getElementById("synthesize-btn").addEventListener("click", runSynthesis);
}

function updateVisibleCards() {
  const gemCard = document.getElementById("gemini-result-card");
  const chirpCard = document.getElementById("chirp-result-card");
  gemCard.classList.toggle("hidden", state.engine === "chirp3_hd");
  chirpCard.classList.toggle("hidden", state.engine === "gemini");
}

function schedulePreview() {
  if (state.previewTimer) clearTimeout(state.previewTimer);
  state.previewTimer = setTimeout(fetchPreview, 120);
}

function buildRequestBody() {
  return {
    text: document.getElementById("script-textarea").value.trim() || "Voltara EX2",
    language_code: state.languageCode,
    pronunciation_mode: state.pronunciationMode,
    voice_name: state.voiceName,
    chirp_control_mode: state.chirpControlMode,
    insert_pauses: state.insertPauses,
    glossary: state.glossary,
    engine: state.engine,
    gemini_model: state.geminiModel,
    style: document.getElementById("gemini-style-input").value,
    speaking_rate: state.speakingRate,
  };
}

async function fetchPreview() {
  const payload = buildRequestBody();
  try {
    const resp = await fetch("/api/preview", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!resp.ok) return;
    const compiled = await parseJsonSafe(resp);
    state.lastCompiled = compiled;
    renderCompiledPreview(compiled);
  } catch (err) {
    console.error("Preview error:", err);
  }
}

function renderCompiledPreview(compiled) {
  const previewEl = document.getElementById("highlighted-preview");
  previewEl.innerHTML = "";
  const text = compiled.display_text || "";
  const matches = compiled.matched_terms || [];

  document.getElementById("match-counter-badge").textContent = formatMatchCount(matches.length);

  let cursor = 0;
  for (const m of matches) {
    if (m.start > cursor) {
      previewEl.appendChild(document.createTextNode(text.slice(cursor, m.start)));
    }
    const span = document.createElement("span");
    span.className = "term-chip";
    span.dataset.cat = m.category || "terminology";
    span.title = t("termTooltip")(m.gemini_replacement, m.chirp_phonetic);
    span.textContent = text.slice(m.start, m.end);
    previewEl.appendChild(span);
    cursor = m.end;
  }
  if (cursor < text.length) {
    previewEl.appendChild(document.createTextNode(text.slice(cursor)));
  }

  document.getElementById("gemini-compiled-preview").textContent =
    compiled.gemini?.tts_transcript || "";

  const chirp = compiled.chirp || {};
  const chirpLabel = document.getElementById("chirp-compiled-label");
  const chirpPre = document.getElementById("chirp-compiled-preview");
  if (chirp.effective_mode === "ssml" && chirp.ssml) {
    chirpLabel.textContent = t("chirpCompiledSsml")(chirp.voice_name);
    chirpPre.textContent = chirp.ssml;
  } else if (chirp.effective_mode === "custom_pronunciations") {
    chirpLabel.textContent = t("chirpCompiledCustomPron")(chirp.voice_name);
    chirpPre.textContent = JSON.stringify(
      {
        text: chirp.text,
        customPronunciations: chirp.custom_pronunciations,
      },
      null,
      2
    );
  } else {
    chirpLabel.textContent = t("chirpCompiledRaw")(chirp.voice_name);
    chirpPre.textContent = chirp.text || "";
  }

  const notesBanner = document.getElementById("compiler-notes");
  const activeNotes =
    state.uiLang === "zh-CN" && compiled.notes_zh?.length > 0
      ? compiled.notes_zh
      : compiled.notes || [];
  if (activeNotes.length > 0) {
    notesBanner.textContent = activeNotes.join(" ");
    notesBanner.classList.remove("hidden");
  } else {
    notesBanner.classList.add("hidden");
  }
}

async function runSynthesis() {
  const btn = document.getElementById("synthesize-btn");
  const statusEl = document.getElementById("synthesis-status");
  const errBanner = document.getElementById("error-banner");

  btn.disabled = true;
  errBanner.classList.add("hidden");
  state.statusKey = "statusSynthesizing";
  statusEl.textContent = t("statusSynthesizing");
  updateVisibleCards();

  try {
    const reqBody = buildRequestBody();
    const resp = await fetch("/api/synthesize", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reqBody),
    });
    const data = await parseJsonSafe(resp);

    if (!resp.ok) {
      throw new Error(data.detail || `HTTP ${resp.status}`);
    }

    if (data.compiled) {
      state.lastCompiled = data.compiled;
      renderCompiledPreview(data.compiled);
    }

    const errs = data.errors || {};
    const errMessages = Object.entries(errs).map(([k, v]) => `${k}: ${v}`);
    if (errMessages.length > 0) {
      errBanner.textContent = errMessages.join(" | ");
      errBanner.classList.remove("hidden");
    }

    if (data.results?.gemini) {
      state.lastResults.gemini = data.results.gemini;
      renderAudioResult("gemini", data.results.gemini, true);
    }
    if (data.results?.chirp3_hd) {
      state.lastResults.chirp3_hd = data.results.chirp3_hd;
      renderAudioResult("chirp", data.results.chirp3_hd, true);
    }

    state.statusKey = "statusComplete";
    statusEl.textContent = t("statusComplete");
  } catch (err) {
    errBanner.textContent = err.message || String(err);
    errBanner.classList.remove("hidden");
    state.statusKey = "statusFailed";
    statusEl.textContent = t("statusFailed");
  } finally {
    btn.disabled = false;
  }
}

function renderAudioResult(prefix, res, rebuildAudioPlayer = true) {
  const headingEl = document.getElementById(`${prefix}-card-heading`);
  const metricsEl = document.getElementById(`${prefix}-metrics`);
  const slotEl = document.getElementById(`${prefix}-player-slot`);
  const jsonEl = document.getElementById(`${prefix}-payload-json`);
  const canvasEl = document.getElementById(`${prefix}-waveform`);

  if (prefix === "gemini") {
    headingEl.textContent = t("geminiResultHeading")(res.model, res.voice);
  } else {
    let modeLabel = t("chirpModeBadgeRaw");
    if (res.effective_control_mode === "ssml") {
      modeLabel = t("chirpModeBadgeSsml");
    } else if (res.effective_control_mode === "custom_pronunciations") {
      modeLabel = t("chirpModeBadgeCustom");
    }
    headingEl.textContent = t("chirpResultHeading")(res.voice, modeLabel);
  }

  metricsEl.innerHTML = "";
  const chipLatency = document.createElement("span");
  chipLatency.className = "metric-chip";
  chipLatency.textContent = formatLatencyMs(res.latency_ms);

  const chipDur = document.createElement("span");
  chipDur.className = "metric-chip";
  chipDur.textContent = formatDurationSec(res.duration_seconds);

  metricsEl.append(chipLatency, chipDur);

  if (!rebuildAudioPlayer) {
    const existingDl = slotEl.querySelector(".download-link");
    if (existingDl) {
      existingDl.textContent = t("downloadWav");
    }
    return;
  }

  const byteChars = atob(res.audio_base64);
  const bytes = new Uint8Array(byteChars.length);
  for (let i = 0; i < byteChars.length; i++) {
    bytes[i] = byteChars.charCodeAt(i);
  }
  const blob = new Blob([bytes], { type: "audio/wav" });
  const blobUrl = URL.createObjectURL(blob);

  slotEl.innerHTML = "";
  const audio = document.createElement("audio");
  audio.controls = true;
  audio.src = blobUrl;
  audio.preload = "auto";

  const dl = document.createElement("a");
  dl.className = "download-link";
  dl.href = blobUrl;
  dl.download = `${prefix}_${state.languageCode}_${state.pronunciationMode}_${res.voice}.wav`;
  dl.textContent = t("downloadWav");

  slotEl.append(audio, dl);
  jsonEl.textContent = JSON.stringify(res.request_payload, null, 2);

  drawPcmWaveform(canvasEl, bytes, prefix === "gemini" ? "#0284c7" : "#059669");
}

function drawPcmWaveform(canvas, wavBytes, strokeColor) {
  if (!canvas || wavBytes.length <= 44) return;
  canvas.classList.remove("hidden");
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  const pcmLen = Math.floor((wavBytes.length - 44) / 2);
  if (pcmLen <= 0) return;
  const view = new DataView(wavBytes.buffer, wavBytes.byteOffset + 44, pcmLen * 2);

  const bars = 128;
  const samplesPerBar = Math.max(1, Math.floor(pcmLen / bars));
  const barWidth = w / bars;

  ctx.fillStyle = strokeColor;
  for (let b = 0; b < bars; b++) {
    let peak = 0;
    const start = b * samplesPerBar;
    const step = Math.max(1, Math.floor(samplesPerBar / 24));
    for (let s = 0; s < samplesPerBar && start + s < pcmLen; s += step) {
      const sample = Math.abs(view.getInt16((start + s) * 2, true)) / 32768.0;
      if (sample > peak) peak = sample;
    }
    const barH = Math.max(2, Math.min(h - 6, peak * (h - 6) * 1.35));
    const x = b * barWidth + 1;
    const y = (h - barH) / 2;
    ctx.fillRect(x, y, Math.max(1.5, barWidth - 2), barH);
  }
}

document.addEventListener("DOMContentLoaded", initApp);
