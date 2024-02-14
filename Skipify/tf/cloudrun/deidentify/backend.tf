terraform {
  backend "gcs" {
    bucket = "cloudrun-demo-dlp"
    prefix = "terraform/state3"
  }
}
