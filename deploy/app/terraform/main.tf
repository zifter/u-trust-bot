locals {
  cloud_run_name = "u-trust-bot-${var.env_name}"

  # TODO
  # https://github.com/hashicorp/terraform-provider-google/issues/9277
  project_hash = "5svpu4bngq"
  region_hash = "lm"
  calculated_service_url = "https://${local.cloud_run_name}-${local.project_hash}-${local.region_hash}.a.run.app"
  service_url = "${var.service_url != "" ? var.service_url : local.calculated_service_url}"
}

resource "google_storage_bucket" "speech2text_workspace" {
  provider = google-beta

  project = var.gcp_project_name
  name          = "${var.gcp_project_name}-speech2text-workspace-${var.env_name}"
  location      = "EU"
  force_destroy = true

  uniform_bucket_level_access = true

  labels     = {
    managed_by = "terraform"
  }
}

resource "random_password" "secret_token" {
  length = 32
  special = false
  keepers = {
    # Generate a new id each time we switch to a new Telegram Token
    telegram_token = var.telegram_token
  }
}

# Create the Cloud Run service
resource "google_cloud_run_service" "run_bot" {
  provider = google-beta

  name = "${local.cloud_run_name}"

  project = var.gcp_project_name
  location = var.gcp_region

  template {
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale"      = "0"
        "autoscaling.knative.dev/maxScale"      = "3"
      }
    }

    spec {
      containers {
        image = "${var.bot_image}"
        env {
          name = "UTRUST_TELEGRAM_TOKEN"
          value = "${var.telegram_token}"
        }
        env {
          name = "UTRUST_SECRET_TOKEN"
          value = "${random_password.secret_token.result}"
        }
        env {
          name = "UTRUST_URL"
          value = "${local.service_url}"
        }
        env {
          name = "UTRUST_SPEECH_TO_TEXT_WORKSPACE"
          value = "${google_storage_bucket.speech2text_workspace.name}"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Allow unauthenticated external users to invoke the service
resource "google_cloud_run_service_iam_member" "run_bot_allow_all_users" {
  provider = google-beta

  project = var.gcp_project_name
  service  = google_cloud_run_service.run_bot.name
  location = google_cloud_run_service.run_bot.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
