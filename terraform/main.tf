locals {
  service_account = "service-send-facture-spotify@send-facture-spotify.iam.gserviceaccount.com"
  project_id = "send-facture-spotify"
  gcp_region = "europe-west1"
}
resource "google_cloud_run_service" "run-send-receipt-spotify" {
  name     = "run-send-receipt-spotify"
  location = local.gcp_region
  template {
    spec {
      service_account_name = "service-send-facture-spotify@send-facture-spotify.iam.gserviceaccount.com"
      containers {
        command = ["./app/main/cron/run-app.sh"]
        image = "eu.gcr.io/send-facture-spotify/cron-send-receipt-spotify@sha256:efd9fee18445493c4382ccc0952aa5b9f7f9995ada38b574aac6a15fdac6bf78"
        ports {
          container_port = 8080
        }
        env {
          name = "FB_THREAD_ID"
          value = "100003782897932"
        }
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_scheduler_job" "scheduler-send-receipt-spotify" {
  name             = "monthly-report-spotify-receipt"
  description      = "It will send monthly receipt to messenger group"
  schedule         = "59 10 28-31 * *"
  time_zone        = "CET"
  http_target {
    http_method = "GET"
      uri = google_cloud_run_service.run-send-receipt-spotify.status[0].url
    oidc_token {
      service_account_email = local.service_account
    }
  }
}