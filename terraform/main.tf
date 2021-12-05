locals {
  service_account = "service-send-facture-spotify@send-facture-spotify.iam.gserviceaccount.com"
  thread_id       = "6947468915279299"
  project_id      = "send-facture-spotify"
  cre_secret_id   = "gmail_credentials"
  tok_secret_id   = "gmail_token"
  ses_secret_id   = "facebook_session"
  log_secret_id   = "facebook_login"
  gcp_region      = "europe-west1"
  imap_url        = "imap.gmail.com"
  # gmail content
  email_sender    = "service@paypal.fr"
  email_subject   = "reçu, Spotify AB"
  email_key_words = "transaction, support@spotify.com"
}
resource "google_cloud_run_service" "run-send-receipt-spotify" {
  name     = "run-send-receipt-spotify"
  location = local.gcp_region
  template {
    spec {
      service_account_name = "service-send-facture-spotify@send-facture-spotify.iam.gserviceaccount.com"
      containers {
        command = ["./app/main/script/run-app.sh"]
        image   = "eu.gcr.io/send-facture-spotify/cron-send-receipt-spotify:latest"
        ports {
          container_port = 8080
        }
        env {
          name  = "FB_THREAD_ID"
          value = local.thread_id
        }
        env {
          name  = "PROJECT_ID"
          value = local.project_id
        }
        env {
          name  = "CRE_SECRET_ID"
          value = local.project_id
        }
        env {
          name  = "TOK_SECRET_ID"
          value = local.tok_secret_id
        }
        env {
          name  = "SES_SECRET_ID"
          value = local.ses_secret_id
        }
        env {
          name  = "LOG_SECRET_ID"
          value = local.log_secret_id
        }
        env {
          name  = "IMAP_URL"
          value = local.imap_url
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
  name        = "monthly-report-spotify-receipt"
  description = "It will send monthly receipt to messenger group"
  schedule    = "59 10 28-31 * *"
  time_zone   = "CET"
  http_target {
    http_method = "GET"
    uri         = "${google_cloud_run_service.run-send-receipt-spotify.status[0].url}/?sender=${local.email_sender}&subject=${local.email_subject}&key_words=${local.email_key_words}"
    oidc_token {
      service_account_email = local.service_account
    }
  }
}