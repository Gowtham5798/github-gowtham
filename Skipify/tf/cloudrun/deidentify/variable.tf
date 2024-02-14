# mandatory
variable "project" {
  default = "skipify-demo"
  description = "GCP project ID"
}

variable "region" {
  default = "us-central1"
  description = "GCP region where the service will be launched"
}

variable "account_id"{
  default = "cloudrun-deidentify-05"
  description = "Cloud Run service account ID"
}

variable "name" {
  default = "cloudrun-srv-deidentify"
  description = "Cloud Run service name"
}

# mandatory
variable "image" {
  default = ""
  description = "Docker image path in GCR"
}

# mandatory
variable "container_port" {
  default = "5000"
  description = "Port on which the container listens"
}

# mandatory
variable "service_account"{
  default ="cloud-run-test@skipify-demo.iam.gserviceaccount.com"
  description = "Cloud Run service account used by Cloud Run"
}


variable "percent" {
  default = "100"
  description = "Traffic allocation percentage"
}

# v1 version cloud run option
# variable "latest_revision" {
#   default = "true"
# }


variable "cpu" {
  default = "20"
  description = "CPU allocation for Cloud Run"
}

variable "memory" {
  default = "1024Mi"
  description = "Memory allocation for Cloud Run"
}

variable "type" {
  default = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  description = "Traffic allocation type"
}

# mandatory
variable "role" {
  default = "roles/run.invoker"
  description = "Role for invoker permissions"
}
