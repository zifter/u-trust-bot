resource "google_storage_bucket" "speech2text_workspace" {
  provider = google-beta

  project = var.gcp_project_name
  name          = "${var.global_prefix}-speech2text-workspace-${var.env_name}"
  location      = "EU"
  force_destroy = true

  uniform_bucket_level_access = true

  labels     = {
    managed_by = "terraform"
  }
}

resource "random_password" "secret_token" {
  length = 16
  keepers = {
    # Generate a new id each time we switch to a new Telegram Token
    telegram_token = var.telegram_token
  }
}

# Create the Cloud Run service
resource "google_cloud_run_service" "run_bot" {
  provider = google-beta

  name = "u-trust-bot"

  project = var.gcp_project_name
  location = var.gcp_region

  template {
    spec {
      containers {
        image = "${var.bot_image}"
        env {
          name = "UTRUST_TELEGRAM_TOKEN"
          value = "${var.telegram_token}"
        }
        env {
          name = "UTRUST_SECRET_TOKEN"
          value = "${random_password.secret_token.id}"
        }
        env {
          name = "UTRUST_URL"
          value = "${var.service_url}"
        }
        env {
          name = "UTRUST_SPEECH_TO_TEXT_WORKSPACE"
          value = "${google_storage_bucket.speech2text_workspace.name}"
        }
      }
    }
  }

  metadata {
    annotations = {
      "autoscaling.knative.dev/max-scale" = "2"
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

locals {
  service_url = google_cloud_run_service.run_bot.status[0].url
  set_bot_url_webhook = "https://api.telegram.org/bot${var.telegram_token}/setWebhook?url=${local.service_url}"
}

# Set url webhook for telegram
data "curl" "set_bot_webhook" {
  http_method = "GET"
  uri = "${local.set_bot_url_webhook}"
}
