# Enables the Cloud Run API
resource "google_project_service" "run_api" {
  provider = google-beta

  project = var.gcp_project_name
  service = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "speech_api" {
  provider = google-beta

  project = var.gcp_project_name
  service = "speech.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifactregistry_api" {
  provider = google-beta

  project = var.gcp_project_name
  service = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "iam_api" {
  provider = google-beta

  project = var.gcp_project_name
  service = "iam.googleapis.com"
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "artifact_registry" {
  provider = google-beta

  project = var.gcp_project_name
  location      = var.gcp_region
  repository_id = "u-trust-cr"
  description   = "Container Registry"
  format        = "DOCKER"

  depends_on = [
    google_project_service.artifactregistry_api,
  ]

  labels     = {
    managed_by = "terraform"
  }
}

resource "google_service_account" "deployer" {
  provider = google-beta

  project = var.gcp_project_name
  account_id   = "sa-deployer"
  display_name = "Deployer Service Account"
}

resource "google_service_account_key" "deployer_key" {
  service_account_id = google_service_account.deployer.name

  depends_on = [
    google_project_service.iam_api
  ]
}

resource "google_artifact_registry_repository_iam_member" "deployer_iam" {
  provider = google-beta

  project = var.gcp_project_name
  location = google_artifact_registry_repository.artifact_registry.location
  repository = google_artifact_registry_repository.artifact_registry.name
  role   = "roles/artifactregistry.writer"
  member = "serviceAccount:${google_service_account.deployer.email}"
}

resource "google_storage_bucket" "tf_state_prod" {
  provider = google-beta

  project       = var.gcp_project_name
  name          = var.tf_state_prod_bucket
  location      = "EU"
  force_destroy = true

  uniform_bucket_level_access = true

  labels     = {
    managed_by = "terraform"
  }
}

resource "google_storage_bucket" "tf_state_dev" {
  provider = google-beta

  project       = var.gcp_project_name
  name          = var.tf_state_dev_bucket
  location      = "EU"
  force_destroy = true

  uniform_bucket_level_access = true

  labels     = {
    managed_by = "terraform"
  }
}

resource "github_actions_secret" "gcp_project_name" {
  repository       = "${var.github_repository}"
  secret_name      = "GCP_PROJECT_NAME"
  plaintext_value  = "${var.gcp_project_name}"
}

resource "github_actions_secret" "deployer_google_credentials" {
  repository       = "${var.github_repository}"
  secret_name      = "GOOGLE_CREDENTIALS"
  plaintext_value  = google_service_account_key.deployer_key.private_key
}

resource "github_actions_secret" "artifact_registry_url" {
  repository       = "${var.github_repository}"
  secret_name      = "GCP_ARTIFACT_REGISTRY"
  plaintext_value  = "${local.artifact_registry_url}"
}

resource "github_actions_secret" "tf_state_bucket_dev" {
  repository       = "${var.github_repository}"
  secret_name      = "TF_STATE_APP_BUCKET_DEV"
  plaintext_value  = "${google_storage_bucket.tf_state_dev.name}"
}

locals {
  artifact_registry_url = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_name}/${google_artifact_registry_repository.artifact_registry.repository_id}"
}
