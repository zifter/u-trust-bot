variable "gcp_sa_credentials" {
  type        = string
  description = "Service Account key file"
}

variable "gcp_project_name" {
  default     = ""
  type        = string
  description = "GCP Project Name"
}

variable "gcp_region" {
  default = "europe-central2"
}

variable "gcp_zone" {
  default = "europe-central2-c"
}

variable "speech2text_bucket" {
}

terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.68.0"
    }
  }
  backend "gcs" {
  }
}

provider "google" {
  credentials = file(var.gcp_sa_credentials)

  project = var.gcp_project_name
  region  = var.gcp_region
  zone    = var.gcp_zone
}

# Enables the Cloud Run API
resource "google_project_service" "run_api" {
  project = var.gcp_project_name

  service = "run.googleapis.com"

  disable_on_destroy = false
}

resource "google_project_service" "speech_api" {
  project = var.gcp_project_name

  service = "speech.googleapis.com"

  disable_on_destroy = false
}

resource "google_storage_bucket" "speech2text_workspace" {
  project = var.gcp_project_name

  name          = var.speech2text_bucket
  location      = "EU"
  force_destroy = true

  uniform_bucket_level_access = true
}

# Create the Cloud Run service
# resource "google_cloud_run_service" "run_service" {
#   name = "app"
#   location = "us-central1"
#
#   template {
#     spec {
#       containers {
#         image = "gcr.io/google-samples/hello-app:1.0"
#       }
#     }
#   }
#
#   traffic {
#     percent         = 100
#     latest_revision = true
#   }
#
#   # Waits for the Cloud Run API to be enabled
#   depends_on = [google_project_service.run_api]
# }

# # Allow unauthenticated users to invoke the service
# resource "google_cloud_run_service_iam_member" "run_all_users" {
#   service  = google_cloud_run_service.run_service.name
#   location = google_cloud_run_service.run_service.location
#   role     = "roles/run.invoker"
#   member   = "allUsers"
# }

# # Display the service URL
# output "service_url" {
#   value = google_cloud_run_service.run_service.status[0].url
# }