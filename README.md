# Multilingual & Custom Terminology Pronunciation Studio (`Gemini 3.8 TTS` + `Chirp 3 HD`)

Interactive web studio demonstrating multilingual code-switching and custom brand/terminology/acronym pronunciation control across **Spanish (`es-ES`, `es-US`)**, **Portuguese (`pt-BR`, `pt-PT`)**, and **Chinese (`cmn-CN`)**, featuring **`Voltara EX2`** alongside technical acronyms (`SUV`, `OTA`, `WLTP`, `LiDAR`, `SQL`, `Apple CarPlay`).

## Key Capabilities
- **Dual-Engine Side-by-Side Comparison**:
  - **Gemini 3.8 TTS (`gemini-3.8-flash-tts`, `gemini-3.8-flash-lite-tts`)**: Served via Vertex AI Global (`aiplatform.googleapis.com`, `location="global"`), leveraging dual-track pre-TTS normalization (`display_text` vs. `tts_transcript`), native intra-sentence multimodal code-switching, `speechMetadata.style`, and `<short pause>` tags.
  - **Chirp 3 HD (`<locale>-Chirp3-HD-<Voice>`)**: Served via Cloud Text-to-Speech (`texttospeech.googleapis.com`), providing fine-grained phonetic control via `CustomPronunciations` (`PHONETIC_ENCODING_IPA` / `X_SAMPA` for `es-*` & `pt-BR`; `PHONETIC_ENCODING_PINYIN` for `cmn-CN`) and synchronous SSML (`<phoneme>`, `<say-as>`, `<sub>`, and mid-sentence `<voice name="en-US-Chirp3-HD-{Voice}">`).
- **Pronunciation Mode Toggle**: Switch between **Standard English** (`"Vol-tah-rah E-X two"`), **Native Language** (`"Bol-ta-ra E equis dos"` / `"Vol-tá-ra É xis dois"` / `"沃尔塔拉 E-X 二"`), and **Raw Baseline**.
- **Shared Prebuilt Voice Selector**: 12 prebuilt star/moon voices (`Kore`, `Puck`, `Aoede`, `Charon`, `Leda`, `Zephyr`, `Fenrir`, `Orus`, `Sulafat`, `Despina`, `Achird`, `Schedar`).

## Running Locally
```bash
export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
export GOOGLE_CLOUD_LOCATION="global"
chmod +x run.sh
./run.sh
```
Open `http://localhost:8080`.

## Docker Compose (Vertex AI ADC)
```bash
docker compose up --build
```
*(Note: Ignore any `GEMINI_API_KEY not set` messages; authentication uses Vertex AI Application Default Credentials mounted into the container.)*

## Deploying to Cloud Run (or via Click-to-Deploy Terraform)
See `click-to-deploy/` for the Argolis-compliant Terraform deployment (Artifact Registry, Cloud Run with `INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER`, External HTTPS Load Balancer, Serverless NEG, and Identity-Aware Proxy).

For manual CLI deployment, ensure the Cloud Run runtime service account has **`roles/aiplatform.user`** granted, and pass both `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION="global"`:
```bash
gcloud run deploy gemini-tts-pronunciation \
  --source . \
  --region us-central1 \
  --ingress=internal-and-cloud-load-balancing \
  --no-allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GOOGLE_CLOUD_LOCATION=global
```
