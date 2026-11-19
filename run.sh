#!/usr/bin/env bash
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

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

export CLOUDSDK_ACTIVE_CONFIG_NAME="${CLOUDSDK_ACTIVE_CONFIG_NAME:-default}"
export GCLOUD_CONFIG_NAME="${GCLOUD_CONFIG_NAME:-default}"
export GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT:-your-project-id}"
export GOOGLE_CLOUD_LOCATION="global"
export PORT="${PORT:-8080}"

exec "${SCRIPT_DIR}/.venv/bin/uvicorn" app:app --host 0.0.0.0 --port "${PORT}"
