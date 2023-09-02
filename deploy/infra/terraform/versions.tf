terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.80.0"
    }
    github = {
      source  = "integrations/github"
      version = "5.34.0"
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

provider "github" {
  owner = var.github_owner
  token = var.github_token
}