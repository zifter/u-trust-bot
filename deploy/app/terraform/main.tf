locals {
  cloud_run_handler_name = "${var.env_name}-handler"
  cloud_run_job_name = "${var.env_name}-app-migrate"

  # TODO
  # https://github.com/hashicorp/terraform-provider-google/issues/9277
  project_hash = "5svpu4bngq"
  region_hash = "lm"
  calculated_service_url = "https://${local.cloud_run_handler_name}-${local.project_hash}-${local.region_hash}.a.run.app"

  service_url = "${var.service_url != "" ? var.service_url : local.calculated_service_url}"
}

resource "google_storage_bucket" "speech2text_workspace" {
  provider = google-beta

  project = var.gcp_project_name
  name          = "${var.gcp_project_name}-speech2text-workspace-${var.env_name}"
  location      = "EU"
  force_destroy = true

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }

  labels = {
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

  name = "${local.cloud_run_handler_name}"

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
        args = ["webhook"]
        env {
          name = "UTRUST_ENVIRONMENT_NAME"
          value = "${var.env_name}"
        }
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

resource "google_cloud_run_v2_job" "app_migrate_job" {
  provider     = google-beta
  name         = "${local.cloud_run_job_name}"
  project      = var.gcp_project_name
  location     = var.gcp_region

  template {
    template {
      timeout = "30s"
      containers {
        image = "${var.bot_image}"
        args  = ["app-migrate"]
        env {
          name  = "UTRUST_ENVIRONMENT_NAME"
          value = "${var.env_name}"
        }
        env {
          name  = "UTRUST_TELEGRAM_TOKEN"
          value = "${var.telegram_token}"
        }
        env {
          name  = "UTRUST_SPEECH_TO_TEXT_WORKSPACE"
          value = "${google_storage_bucket.speech2text_workspace.name}"
        }
      }
    }
  }

  lifecycle {
    ignore_changes = [
      launch_stage,
    ]
  }
}

resource "null_resource" "trigger_app_migrate_job" {
  provisioner "local-exec" {
    command = "gcloud alpha run jobs execute ${local.cloud_run_job_name} --wait --project=${var.gcp_project_name} --region=${var.gcp_region}"
  }

  depends_on = [google_cloud_run_v2_job.app_migrate_job]
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
