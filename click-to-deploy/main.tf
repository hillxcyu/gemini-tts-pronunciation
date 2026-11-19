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

data "google_project" "current" {
  project_id = var.project_id
}

locals {
  services = [
    "aiplatform.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "compute.googleapis.com",
    "iam.googleapis.com",
    "iap.googleapis.com",
    "logging.googleapis.com",
    "run.googleapis.com",
    "serviceusage.googleapis.com",
    "texttospeech.googleapis.com",
  ]

  runtime_roles = [
    "roles/aiplatform.user",
    "roles/logging.logWriter",
    "roles/serviceusage.serviceUsageConsumer",
  ]

  effective_project_number = coalesce(var.project_number, data.google_project.current.number)
  effective_image = coalesce(
    var.container_image,
    "${var.data_location}-docker.pkg.dev/${var.project_id}/${var.artifact_repo}/${var.service_name}:latest",
  )
  iap_audience = "/projects/${local.effective_project_number}/global/backendServices/${google_compute_backend_service.web.generated_id}"
}

resource "google_project_service" "enabled" {
  for_each           = toset(local.services)
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "images" {
  project       = var.project_id
  location      = var.data_location
  repository_id = var.artifact_repo
  format        = "DOCKER"
  description   = "Container images for Multilingual Pronunciation Studio"
  depends_on    = [google_project_service.enabled]
}

resource "google_service_account" "runtime" {
  project      = var.project_id
  account_id   = "${var.service_name}-sa"
  display_name = "Multilingual Pronunciation Studio Cloud Run Runtime SA"
  depends_on   = [google_project_service.enabled]
}

resource "google_project_iam_member" "runtime_roles" {
  for_each = toset(local.runtime_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.runtime.email}"
}

resource "google_cloud_run_v2_service" "web" {
  project             = var.project_id
  name                = var.service_name
  location            = var.data_location
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {
    service_account = google_service_account.runtime.email
    timeout         = "300s"

    scaling {
      min_instance_count = 0
      max_instance_count = 4
    }

    containers {
      image = local.effective_image

      resources {
        limits = {
          cpu    = "2"
          memory = "1Gi"
        }
      }

      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }

      env {
        name  = "GOOGLE_CLOUD_LOCATION"
        value = "global"
      }

      env {
        name  = "CLOUD_RUN_REGION"
        value = var.data_location
      }

      env {
        name  = "IAP_EXPECTED_AUDIENCE"
        value = local.iap_audience
      }
    }
  }

  depends_on = [google_project_iam_member.runtime_roles]
}

resource "google_project_service_identity" "iap" {
  provider   = google-beta
  project    = var.project_id
  service    = "iap.googleapis.com"
  depends_on = [google_project_service.enabled]
}

resource "google_cloud_run_v2_service_iam_member" "iap_invoker" {
  project  = var.project_id
  location = google_cloud_run_v2_service.web.location
  name     = google_cloud_run_v2_service.web.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_project_service_identity.iap.email}"
}

# External HTTPS Application Load Balancer + Serverless NEG + Backend IAP
resource "google_compute_global_address" "web" {
  project    = var.project_id
  name       = "${var.service_name}-ip"
  depends_on = [google_project_service.enabled]
}

resource "google_compute_region_network_endpoint_group" "web" {
  project               = var.project_id
  name                  = "${var.service_name}-neg"
  region                = var.data_location
  network_endpoint_type = "SERVERLESS"

  cloud_run {
    service = var.service_name
  }

  depends_on = [google_project_service.enabled]
}

resource "google_compute_backend_service" "web" {
  project               = var.project_id
  name                  = "${var.service_name}-backend"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  protocol              = "HTTPS"
  timeout_sec           = 300

  backend {
    group = google_compute_region_network_endpoint_group.web.id
  }

  lifecycle {
    ignore_changes = [iap]
  }
}

resource "google_compute_url_map" "web" {
  project         = var.project_id
  name            = "${var.service_name}-urlmap"
  default_service = google_compute_backend_service.web.id
}

resource "google_compute_managed_ssl_certificate" "web" {
  project = var.project_id
  name    = "${var.service_name}-cert"

  managed {
    domains = [var.lb_domain]
  }

  depends_on = [google_project_service.enabled]
}

resource "google_compute_target_https_proxy" "web" {
  project          = var.project_id
  name             = "${var.service_name}-https-proxy"
  url_map          = google_compute_url_map.web.id
  ssl_certificates = [google_compute_managed_ssl_certificate.web.id]
}

resource "google_compute_global_forwarding_rule" "https" {
  project               = var.project_id
  name                  = "${var.service_name}-https"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  ip_address            = google_compute_global_address.web.id
  port_range            = "443"
  target                = google_compute_target_https_proxy.web.id
}

resource "google_compute_url_map" "redirect" {
  project = var.project_id
  name    = "${var.service_name}-http-redirect"

  default_url_redirect {
    https_redirect         = true
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
  }

  depends_on = [google_project_service.enabled]
}

resource "google_compute_target_http_proxy" "redirect" {
  project = var.project_id
  name    = "${var.service_name}-http-proxy"
  url_map = google_compute_url_map.redirect.id
}

resource "google_compute_global_forwarding_rule" "http" {
  project               = var.project_id
  name                  = "${var.service_name}-http"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  ip_address            = google_compute_global_address.web.id
  port_range            = "80"
  target                = google_compute_target_http_proxy.redirect.id
}
