# Multilingual & Brand Terminology Pronunciation Studio — Seller Demo Guide

## Executive Summary & Pitch Context

- **Target Buyer Personas:** Head of Localization, VP of Digital Experience, Automotive / Consumer Electronics Product Marketing Lead, Contact Center Architect, Media & Entertainment Studio Director
- **Customer Pain Point:** Global brands launching products across Spanish, Portuguese, and Mandarin markets struggle with text-to-speech (TTS) engines that mispronounce flagship brand names (e.g., reading `Voltara EX2` with localized Spanish `J`/`B` or garbled letters) and technical acronyms (`SUV`, `OTA`, `WLTP`, `LiDAR`, `SQL`, `Apple CarPlay`), forcing expensive manual studio re-recordings or brittle post-processing.
- **Value Proposition:** Side-by-side live studio demonstrating how Google Cloud's **Gemini 3.8 TTS** (`gemini-3.8-flash-tts`, `gemini-3.8-flash-lite-tts`) and **Chirp 3 HD** (`<locale>-Chirp3-HD-<Voice>`) deliver zero-shot, phoneme-accurate multilingual code-switching and customizable brand/acronym governance—eliminating studio dubbing bottlenecks and cutting localization turnaround from weeks to seconds.
- **Estimated Demo Duration:** 10–15 minutes

## How to Build

This section walks through how `gemini-tts-pronunciation` is architected and built end-to-end on Google Cloud using **FastAPI**, **Vertex AI Gemini 3.8 TTS (`location="global"`)**, **Cloud Text-to-Speech Chirp 3 HD**, and **Cloud Run behind Identity-Aware Proxy (IAP)**.

### Step 1: Scaffold the Project & Dependencies
- Application dependencies are declared in `requirements.txt` (`fastapi`, `uvicorn`, `jinja2`, `pydantic`, `httpx`, `google-auth`, `requests`) and pinned with SHA-256 hashes in `click-to-deploy/requirements.txt` for supply-chain security.
- Container packaging is defined in `Dockerfile` and `click-to-deploy/Dockerfile` using `python:3.12-slim` with `ffmpeg` for WAV container inspection and non-root `appuser` execution on port `8080`.

### Step 2: Build the Pronunciation Lexicon & Compiler (`glossary_data.py`, `pronunciation_engine.py`)
- `glossary_data.py` defines supported language families (`es-ES`, `es-US`, `pt-BR`, `pt-PT`, `cmn-CN`), 12 shared prebuilt voice personas (`Kore`, `Puck`, `Aoede`, `Charon`, `Leda`, `Zephyr`, `Fenrir`, `Orus`, `Sulafat`, `Despina`, `Achird`, `Schedar`), preset multilingual scripts, and `DEFAULT_GLOSSARY` entries with bidirectional **Standard English** vs. **Native Language** phonetic rules.
- `pronunciation_engine.py` implements `compile_pronunciation()` using longest-first span matching (`Voltara EX2` ahead of `Voltara`) to output:
  1. **Gemini 3.8 TTS Dual-Track Transcript**: Clean `display_text` for UI subtitles alongside a phonetically respelled `tts_transcript` with optional `<short pause>` tags and `speechMetadata.style`.
  2. **Chirp 3 HD Phonetic Payloads**: Either synchronous SSML (`<speak>`, `<phoneme alphabet="ipa">`, `<say-as>`, `<sub>`, and mid-sentence `<voice name="en-US-Chirp3-HD-{Voice}">` switching) or `CustomPronunciations` (`PHONETIC_ENCODING_IPA` for `es-*` and `pt-BR`; `PHONETIC_ENCODING_PINYIN` for `cmn-CN`).

### Step 3: Orchestrate Async Synthesis & Web UI (`tts_clients.py`, `app.py`, `templates/index.html`, `static/app.js`)
- `tts_clients.py` manages Google Cloud Application Default Credentials (`GoogleAuthManager`) and executes parallel async calls to Vertex AI (`aiplatform.googleapis.com` global endpoint for Gemini 3.8 TTS) and Cloud Text-to-Speech (`texttospeech.googleapis.com` for Chirp 3 HD), normalizing audio responses into RIFF WAV (`24kHz`, `pcm_s16le`).
- `app.py` exposes `/healthz`, `/api/config`, `/api/preview`, and `/api/synthesize` (`engine="compare"` runs both engines concurrently via `asyncio.gather`).
- `templates/index.html` and `static/app.js` render a bilingual (`EN` / `CN`) side-by-side comparison workbench with live compiled payload inspection and an interactive custom glossary editor.

### Step 4: Test & Deploy to Google Cloud (`tests/`, `click-to-deploy/`)
- Run unit and live synthesis integration tests with `python -m unittest discover -s tests -v`.
- Deploy via `click-to-deploy/` Terraform, which provisions Artifact Registry, a least-privilege runtime service account, Cloud Run (`INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER`), and an External HTTPS Application Load Balancer with Serverless NEG and Identity-Aware Proxy (IAP).

## Pillar 1: Setup & Deployment Instructions

### 1.1 Prerequisites & IAM Permissions
- **GCP Environment:** Google Cloud project with billing enabled.
- **Required IAM Roles for Deployment:** `roles/owner` or (`roles/run.admin`, `roles/artifactregistry.admin`, `roles/compute.loadBalancerAdmin`, `roles/iam.serviceAccountAdmin`, `roles/serviceusage.serviceUsageAdmin`).
- **Required Runtime Service Account Roles:** `roles/aiplatform.user`, `roles/logging.logWriter`, `roles/serviceusage.serviceUsageConsumer`.
- **Required APIs:**
  - Vertex AI API (`aiplatform.googleapis.com`)
  - Cloud Text-to-Speech API (`texttospeech.googleapis.com`)
  - Cloud Run Admin API (`run.googleapis.com`)
  - Artifact Registry API (`artifactregistry.googleapis.com`)
  - Compute Engine API (`compute.googleapis.com`)
  - Identity-Aware Proxy API (`iap.googleapis.com`)

### 1.2 Option A: One-Click Deployment via Click-to-Deploy (Recommended)
1. Navigate to the demo listing and click **Deploy Demo (Click-to-Deploy)**.
2. Select your target GCP organization and project.
3. Wait approximately **5 minutes** for Terraform provisioning to complete.

### 1.3 Option B: Manual CLI / Terraform Deployment
```bash
export PROJECT_ID="your-project-id"
export REGION="us-central1"

# 1. Build and push container image to Artifact Registry
gcloud artifacts repositories create tts-studio-images \
  --repository-format=docker \
  --location="${REGION}" \
  --project="${PROJECT_ID}"

gcloud builds submit \
  --tag "${REGION}-docker.pkg.dev/${PROJECT_ID}/tts-studio-images/gemini-tts-pronunciation:latest" \
  --project="${PROJECT_ID}"

# 2. Provision Cloud Run + External HTTPS ALB + IAP via Terraform
cd click-to-deploy
terraform init
terraform apply \
  -var="project_id=${PROJECT_ID}" \
  -var="data_location=${REGION}"
```

### 1.4 Deployment Verification
Verify the Cloud Run service and load balancer are healthy before your customer call:

```bash
gcloud run services list --project="${PROJECT_ID}" --region="${REGION}"
terraform -chdir=click-to-deploy output app_url
```

### 1.5 Teardown & Cost Cleanup
To avoid ongoing compute or load-balancer charges after your customer session:

```bash
cd click-to-deploy
terraform destroy -var="project_id=${PROJECT_ID}" -var="data_location=${REGION}"
```

## Pillar 2: How to Access the Demo

### 2.1 Retrieving Entry Point URLs
- **Existing Live Application:** Open `https://gemini-tts-pronunciation-440790012685.asia-east1.run.app/`
- **From Self-Deployed Terraform:** Run `terraform -chdir=click-to-deploy output -raw app_url` (or `lb_ip`).
- **Local Development:** Run `./run.sh` after setting `GOOGLE_CLOUD_PROJECT` and open `http://localhost:8080`.

### 2.2 Credentials & Authentication
- **Live / Self-Deployed Cloud Run:** Protected by Google Identity-Aware Proxy (IAP) or Cloud Run IAM. Sign in with an authorized `@google.com` or project IAM user account.
- **Local Development:** Uses Application Default Credentials (`gcloud auth application-default login`). No separate in-app username or password is required.

### 2.3 Expected Initial Landing State
Upon opening the application URL, confirm you see:
- The **Multilingual & Custom Terminology Pronunciation Studio** header with an `EN | CN` UI language toggle and the GCP metadata badge showing your project ID and `location: global`.
- Four top control groups (**1. Main Language**, **2. Brand, Terminology & Acronym Pronunciation**, **3. Prebuilt Voice Persona**, **4. Synthesis Mode**).
- The **Voltara EX2** Spanish launch preset pre-loaded in the script editor with highlighted custom term spans and live compiled previews for both **Gemini 3.8 TTS** and **Chirp 3 HD**.

## Demo Walkthrough (Pillar 3 & Pillar 4: Step-by-Step Walkthrough & Seller Talking Script)

### Opening Discovery Hook (Before Sharing Screen)

> **What to Say:** *"Global product teams tell us their biggest voice-AI bottleneck isn't generating speech—it's getting brand names, model numbers, and technical acronyms like SUV, OTA, or LiDAR pronounced consistently across Spanish, Portuguese, and Mandarin without booking human voice talent for every software release. How does your team currently handle brand and terminology pronunciation across markets?"*

### Step 1: Establish the Baseline Problem (Raw Uncontrolled vs. Standard English)
- **What to Do (Click Sequence):**
  1. Confirm **1. Main Language** is set to **Spanish (`es-ES`)** and the preset **Voltara EX2 Urban EV Launch** is selected.
  2. Under **2. Brand, Terminology & Acronym Pronunciation**, click **Raw (Uncontrolled)**.
  3. Click **Synthesize & Compare Audio** and play both audio cards.
  4. Now switch to **Standard English** and click **Synthesize & Compare Audio** again.
- **Expected Visual Outcome:** In **Raw** mode, the compiled preview shows zero term overrides. In **Standard English** mode, `Voltara EX2`, `SUV`, `WLTP`, `Apple CarPlay`, and `OTA` highlight in the script box, Gemini's `parts[].text` respells `Voltara EX2` as `Vol-tah-rah E-X two`, and Chirp 3 HD wraps English brands in `<voice name="en-US-Chirp3-HD-Kore">` with IPA `<phoneme>` tags.
- **What to Say:** *"Watch what happens when we move from Raw baseline to Standard English mode. Notice how our dual-track compiler keeps the on-screen subtitle clean (`Voltara EX2`) while feeding Gemini 3.8 TTS a phonetically respelled track and giving Chirp 3 HD deterministic IPA and mid-sentence `<voice>` switching—all using the exact same voice persona (`Kore`) so there's zero jarring speaker change."*

### Step 2: Switch to Native Localized Pronunciation
- **What to Do (Click Sequence):**
  1. Keep the same Spanish script, and switch **2. Brand, Terminology & Acronym Pronunciation** to **Native Language**.
  2. Under **Chirp 3 HD Phonetic Controls**, select **CustomPronunciations API (IPA / X-SAMPA / Pinyin Lexicon)**.
  3. Click **Synthesize & Compare Audio** and play both outputs.
- **Expected Visual Outcome:** The compiled Gemini preview updates to `Bol-ta-ra E equis dos`, `ese u uve`, and `o te a`. The Chirp 3 HD preview switches to a JSON `customPronunciations` payload using `PHONETIC_ENCODING_IPA`.
- **What to Say:** *"Some markets want English brand pronunciation; others—like Latin America or Brazil—expect localized pronunciation. With one click, we switch from English-style code-switching to native Spanish phonetics, and you can inspect the exact `generateContent` and `text:synthesize` API payloads right below the audio players."*

### Step 3: Showcase Expressive Acting & Micro-Pauses in Gemini 3.8 TTS
- **What to Do (Click Sequence):**
  1. In **Gemini 3.8 TTS Parameters**, type `Warm, energetic automotive launch presenter` into **Turn Delivery Style (`speechMetadata.style`)**.
  2. Check **Insert micro-pause tags before custom terms**.
  3. Click **Synthesize & Compare Audio** and play the Gemini 3.8 TTS card.
- **Expected Visual Outcome:** The compiled Gemini transcript inserts `<short pause>` tags before custom terms, and the audio reflects natural commercial pacing and warmth.
- **What to Say:** *"This is where Gemini 3.8 TTS shines for marketing and media workflows: natural-language style direction via `speechMetadata.style` and inline vocal `<short pause>` tags give you studio-director control without SSML complexity."*

### Step 4: Demonstrate Mandarin Code-Switching & Polyphone Disambiguation (`cmn-CN`)
- **What to Do (Click Sequence):**
  1. Under **1. Main Language**, click **Chinese (`cmn-CN`)**.
  2. Select the preset **Smart Cockpit & Polyphone Control (银行 / 行人 / SQL)**.
  3. Toggle between **Standard English** and **Native Language**, then click **Synthesize & Compare Audio**.
- **Expected Visual Outcome:** In **Native Language** mode, Chirp 3 HD's compiled payload automatically uses `PHONETIC_ENCODING_PINYIN` with tone numbers (`hang2`, `xing2`, `wo4 er3 ta3 la1`), while in **Standard English** mode it automatically falls back to SSML `<voice>` switching for English terms.
- **What to Say:** *"Mandarin introduces polyphones—characters like `行` that sound completely different in `银行` (bank, yínháng) versus `行人` (pedestrian, xíngrén). Chirp 3 HD enforces tone-numbered Pinyin governance, while Gemini 3.8 TTS handles seamless Mandarin-English code-switching for terms like `LiDAR`, `SQL`, and `OTA`."*

### Step 5: Live Custom Lexicon Editing & Closing Pitch
- **What to Do (Click Sequence):**
  1. Scroll to **Custom Terminology, Brand & Acronym Lexicon**, click **+ Add Custom Term**, or edit an existing pronunciation rule live.
  2. Observe the compiled previews update immediately in real time.
- **What to Say:** *"Everything you see is driven by a live lexicon—your localization team can update a brand pronunciation once and deploy it across both Gemini 3.8 TTS for expressive, conversational experiences and Chirp 3 HD for strict, deterministic IVR and compliance governance. Which of your upcoming product launches or contact center workflows could we pilot with a custom lexicon this week?"*

## Troubleshooting & Live-Demo Recovery Tips

| Symptom | Cause | Recovery Action |
| :--- | :--- | :--- |
| **403 / Permission Denied on Synthesis** | Runtime SA missing `roles/aiplatform.user` or Vertex AI API disabled | Grant `roles/aiplatform.user` to the runtime SA and verify `aiplatform.googleapis.com` and `texttospeech.googleapis.com` are enabled. |
| **Gemini 3.8 TTS 404 / Model Not Found** | `GOOGLE_CLOUD_LOCATION` not set to `global` | Ensure `GOOGLE_CLOUD_LOCATION=global` is set in Cloud Run env vars (Gemini 3.8 TTS is served from the Vertex AI global endpoint). |
| **IAP Session Expired Banner** | Corp/IAP login cookie timed out during a long call | Refresh the browser tab (`Cmd+R` / `Ctrl+R`) to re-authenticate with IAP; the studio reloads cleanly in under 2 seconds. |
| **Slow First Request (Cold Start)** | Cloud Run scaled to zero (`min_instance_count = 0`) | Click **Synthesize & Compare Audio** once 2 minutes before joining the customer call to warm up the container. |
