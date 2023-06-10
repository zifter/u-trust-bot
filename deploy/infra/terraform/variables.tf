variable "gcp_sa_credentials" {
  type        = string
  description = "Service Account key file"
}

variable "github_token" {
  type        = string
  description = "Github Access Token"
}

variable "github_repository" {
  type        = string
  description = "Github Repository"
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

variable "tf_state_prod_bucket" {
  default = "u-trust-app-tf-state-prod"
}

variable "tf_state_dev_bucket" {
  default = "u-trust-app-tf-state-dev"
}
