variable "gcp_sa_credentials" {
  type        = string
  description = "Service Account key file path"
}

variable "gcp_project_name" {
  type        = string
  description = "GCP Project Name"
}

variable "gcp_region" {
  default = "europe-central2"
}

variable "gcp_zone" {
  default = "europe-central2-c"
}

variable "env_name" {}
variable "telegram_token" {}
variable "service_url" {}

variable "bot_image" {}

