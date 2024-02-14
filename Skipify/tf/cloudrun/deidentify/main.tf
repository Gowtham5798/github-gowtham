provider "google" {
  project = var.project # Replace with your Google Cloud project ID
  region  = var.region  # Replace with your desired region
}
resource "google_service_account" "service_account" {
  account_id = var.account_id
}

data "google_iam_role" "role1" {
  name = "roles/cloudkms.cryptoKeyEncrypter"
}

data "google_iam_role" "role2" {
  name = "roles/dlp.user"
}

data "google_iam_role" "role3" {
  name = "roles/secretmanager.secretAccessor"
}

data "google_iam_role" "role4" {
  name = "roles/serviceusage.serviceUsageConsumer"
}

data "google_iam_role" "role5" {
  name = "roles/secretmanager.secretVersionManager"
}

resource "google_project_iam_binding" "iam_binding1" {
  project = var.project
  role    = data.google_iam_role.role1.name
  members = ["serviceAccount:${google_service_account.service_account.email}"]
}

resource "google_project_iam_binding" "iam_binding2" {
  project = var.project
  role    = data.google_iam_role.role2.name
  members = ["serviceAccount:${google_service_account.service_account.email}"]
}

resource "google_project_iam_binding" "iam_binding3" {
  project = var.project
  role    = data.google_iam_role.role3.name
  members = ["serviceAccount:${google_service_account.service_account.email}"]
}

resource "google_project_iam_binding" "iam_binding4" {
  project = var.project
  role    = data.google_iam_role.role4.name
  members = ["serviceAccount:${google_service_account.service_account.email}"]
}

resource "google_project_iam_binding" "iam_binding5" {
  project = var.project
  role    = data.google_iam_role.role5.name
  members = ["serviceAccount:${google_service_account.service_account.email}"]
}


output "the_role_permissions" {
  value = concat(
    data.google_iam_role.role1.included_permissions,
    data.google_iam_role.role2.included_permissions,
    data.google_iam_role.role3.included_permissions,
    data.google_iam_role.role4.included_permissions,
    data.google_iam_role.role5.included_permissions
  )
}

resource "google_cloud_run_v2_service" "cloudrun-deidentify" {
  name     = var.name
  location = var.region

  template {
    containers {
      image = var.image
      resources {
        limits = {
          cpu    = var.cpu
          memory = var.memory
        }
      }
      ports {
        container_port = var.container_port
      }
    }
    service_account = google_service_account.service_account.email
    # service_account = var.service_account
  }

  traffic {
    type = var.type
    # latest_revision = var.latest_revision
    percent = var.percent
  }
}

# Create public access
data "google_iam_policy" "noauth" {
  binding {
    role = var.role
    members = [
      "allUsers",
    ]
  }
}
# Enable public access on Cloud Run service
resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_v2_service.cloudrun-deidentify.location
  project     = google_cloud_run_v2_service.cloudrun-deidentify.project
  service     = google_cloud_run_v2_service.cloudrun-deidentify.name
  policy_data = data.google_iam_policy.noauth.policy_data
}

# Return service account ID
output "service_account_email" {
  value = resource.google_service_account.service_account.email
}

# Return service URL
output "url" {
  value = "${google_cloud_run_v2_service.cloudrun-deidentify.uri}"
}
