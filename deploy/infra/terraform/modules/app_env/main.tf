data "github_repository" "repo" {
  full_name = "${var.github_owner}/${var.github_repository}"
}

resource "github_repository_environment" "repo_env" {
  environment  = "${var.env_name}"
  repository   = data.github_repository.repo.name

  deployment_branch_policy {
    protected_branches     = true
    custom_branch_policies = false
  }
}

resource "google_storage_bucket" "tf_state_bucket" {
  provider = google-beta

  project       = var.gcp_project_name
  name          = "${var.gcp_project_name}-tf-state-${var.env_name}"
  location      = "EU"
  force_destroy = true

  uniform_bucket_level_access = true

  labels     = {
    managed_by = "terraform"
  }
}

resource "github_actions_environment_secret" "tf_state_bucket" {
  repository       = data.github_repository.repo.name
  environment      = github_repository_environment.repo_env.environment

  secret_name      = "TF_STATE_APP_BUCKET"
  plaintext_value  = "${google_storage_bucket.tf_state_bucket.name}"
}

resource "github_actions_environment_secret" "telegram_token" {
  repository       = data.github_repository.repo.name
  environment      = github_repository_environment.repo_env.environment

  secret_name      = "TF_VAR_telegram_token"
}

resource "github_actions_environment_secret" "service_url" {
  repository       = data.github_repository.repo.name
  environment      = github_repository_environment.repo_env.environment

  secret_name      = "TF_VAR_service_url"
}
