data "google_service_account" "service_account_send_receipt" {
  account_id = "service-send-facture-spotify"
}


#resource "google_project_iam_binding" "project" {
#  project = local.project_id
#  role    = "roles/cloudscheduler.jobs.create"
#  members = [
#    "serviceAccount:${data.google_service_account.service_account_send_receipt.email}"
#  ]
#}
#
#data "google_iam_policy" "policy" {
#  binding {
#    role = "roles/iam.serviceaccounts.actAs"
#
#    members = [
#      "serviceAccount:${data.google_service_account.service_account_send_receipt.email}"
#    ]
#  }
#}