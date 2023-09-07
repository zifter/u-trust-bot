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

resource "google_project_service" "firestore" {
  provider = google-beta

  project = var.gcp_project_name
  service = "firestore.googleapis.com"
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "artifact_registry" {
  provider = google-beta

  project       = var.gcp_project_name
  location      = var.gcp_region
  repository_id = "u-trust-cr"
  description   = "Container Registry"
  format        = "DOCKER"
  cleanup_policy_dry_run = true
  cleanup_policies {
    id     = "keep-release-for-90-days"
    action = "KEEP"
    condition {
      tag_state   = "TAGGED"
      tag_prefixes = ["main"]
      version_name_prefixes = ["v0"]
      newer_than   = "7776000s" # 90 days
    }
  }
  cleanup_policies {
    id     = "keep-main-for-one-day"
    action = "KEEP"
    condition {
      tag_state   = "TAGGED"
      tag_prefixes = ["main"]
      version_name_prefixes = ["v0"]
      newer_than   = "86400s" # 1 day
    }
  }
  cleanup_policies {
    id     = "keep-latest-packages-for-2-hours"
    action = "KEEP"
    condition {
      tag_state    = "TAGGED"
      newer_than   = "720s" #
    }
  }
  cleanup_policies {
    id     = "delete-old-packages"
    action = "DELETE"
    condition {
      tag_state    = "TAGGED"
      older_than   = "720s"
    }
  }

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

resource "google_project_iam_binding" "iam_deployer_bucket_admin" {
  project = "${var.gcp_project_name}"
  role    = "roles/storage.admin"

  members = [
   "serviceAccount:${google_service_account.deployer.email}",
  ]
}

resource "google_project_iam_binding" "iam_deployer_cloud_run_admin" {
  project = "${var.gcp_project_name}"
  role    = "roles/run.admin"

  members = [
   "serviceAccount:${google_service_account.deployer.email}",
  ]
}
resource "google_project_iam_binding" "iam_deployer_servie_account_user" {
  project = "${var.gcp_project_name}"
  role    = "roles/iam.serviceAccountUser"

  members = [
   "serviceAccount:${google_service_account.deployer.email}",
  ]
}

resource "google_project_iam_binding" "iam_deployer_datastore" {
  project = "${var.gcp_project_name}"
  role    = "roles/datastore.owner"

  members = [
   "serviceAccount:${google_service_account.deployer.email}",
  ]
}

resource "google_project_iam_binding" "iam_deployer_artifact_registry" {
  project = "${var.gcp_project_name}"
  role    = "roles/artifactregistry.repoAdmin"

  members = [
   "serviceAccount:${google_service_account.deployer.email}",
  ]
}

resource "google_service_account_key" "deployer_key" {
  service_account_id = google_service_account.deployer.name

  depends_on = [
    google_project_service.iam_api
  ]
}

resource "google_artifact_registry_repository_iam_member" "deployer_iam_artifact_registry" {
  provider = google-beta

  project = var.gcp_project_name
  location = google_artifact_registry_repository.artifact_registry.location
  repository = google_artifact_registry_repository.artifact_registry.name
  role   = "roles/artifactregistry.writer"
  member = "serviceAccount:${google_service_account.deployer.email}"
}

resource "github_actions_secret" "gcp_project_name" {
  repository       = "${var.github_repository}"
  secret_name      = "TF_VAR_gcp_project_name"
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

locals {
  artifact_registry_url = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_name}/${google_artifact_registry_repository.artifact_registry.repository_id}"
}

module "environment_test" {
  source = "./modules/app_env"

  env_name="test"

  github_owner="${var.github_owner}"
  github_token="${var.github_token}"
  github_repository="${var.github_repository}"

  gcp_project_name="${var.gcp_project_name}"
  gcp_region="${var.gcp_region}"
  gcp_zone="${var.gcp_zone}"
}

module "environment_staging" {
  source = "./modules/app_env"

  env_name="staging"

  github_owner="${var.github_owner}"
  github_token="${var.github_token}"
  github_repository="${var.github_repository}"

  gcp_project_name="${var.gcp_project_name}"
  gcp_region="${var.gcp_region}"
  gcp_zone="${var.gcp_zone}"
}

module "environment_prod" {
  source = "./modules/app_env"

  env_name="prod"

  github_owner="${var.github_owner}"
  github_token="${var.github_token}"
  github_repository="${var.github_repository}"

  gcp_project_name="${var.gcp_project_name}"
  gcp_region="${var.gcp_region}"
  gcp_zone="${var.gcp_zone}"
}
