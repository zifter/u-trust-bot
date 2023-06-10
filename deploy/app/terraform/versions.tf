terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.68.0"
    }
    github = {
      source  = "integrations/github"
      version = "5.26.0"
    }
    curl = {
      source = "anschoewe/curl"
      version = "1.0.2"
    }
    random = {
      source = "hashicorp/random"
      version = "3.5.1"
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

provider "curl" {}