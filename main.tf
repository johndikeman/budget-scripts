# Define the Google Cloud Function
# use the google_cloudfunctions2_function format instead
resource "google_cloudfunctions2_function" "csv_labeler" {
  name        = "csv-labeler"
  description = "A function to label CSV files"
  runtime     = "python39"
  available_memory_mb   = 128
  timeout               = 60
  entry_point           = "process_import"
  source_archive_bucket = google_storage_bucket.function_source.name
  source_archive_object = google_storage_bucket_object.function_source.name
  trigger_http          = true
  ingress_settings      = "ALLOW_INTERNAL_ONLY"
  service_account_email = google_service_account.function_sa.email
}
# Define the Cloud Storage Bucket for the function source code
resource "google_storage_bucket" "function_source" {
  name     = "csv-labeler-source"
  location = "US"
}
# Upload the function source code to the bucket
resource "google_storage_bucket_object" "function_source" {
  name   = "llm_main.py"
  bucket = google_storage_bucket.function_source.name
  source = "llm_main.py"
}
# Define the Cloud Storage Bucket for CSV imports
resource "google_storage_bucket" "csv_imports" {
  name     = "csv-imports"
  location = "US"
  uniform_bucket_level_access = true
}
# Define the Service Account for the Cloud Function
resource "google_service_account" "function_sa" {
  account_id   = "csv-labeler-sa"
  display_name = "Service Account for CSV Labeler Function"
}
# Grant the Service Account access to the CSV imports bucket
resource "google_storage_bucket_iam_member" "csv_imports_access" {
  bucket = google_storage_bucket.csv_imports.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.function_sa.email}"
}
# Output the URL of the deployed Cloud Function
output "function_url" {
  value = google_cloudfunctions_function.csv_labeler.https_trigger_url
}

