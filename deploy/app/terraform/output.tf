output "predicted_url" {
  value = local.service_url
}

output "_expected_url" {
  value = google_cloud_run_service.run_bot.status[0].url
}
