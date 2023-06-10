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

variable "global_prefix" {}
variable "env_name" {}

variable "telegram_token" {}
variable "bot_image" {}
variable "service_url" {}

