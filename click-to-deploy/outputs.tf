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

output "app_url" {
  description = "HTTPS entry point URL for the Multilingual Pronunciation Studio behind IAP."
  value       = "https://${var.lb_domain}"
}

output "lb_ip" {
  description = "Static external IP address of the HTTPS Application Load Balancer."
  value       = google_compute_global_address.web.address
}

output "backend_service" {
  description = "Backend service name protected by Identity-Aware Proxy (IAP)."
  value       = google_compute_backend_service.web.name
}

output "iap_audience" {
  description = "Expected x-goog-iap-jwt-assertion audience string."
  value       = local.iap_audience
}

output "cloud_run_service_name" {
  description = "Deployed Cloud Run service name."
  value       = google_cloud_run_v2_service.web.name
}

output "runtime_service_account" {
  description = "Least-privilege runtime service account email."
  value       = google_service_account.runtime.email
}
