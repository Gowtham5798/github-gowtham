# terraform tfvars
image = "gcr.io/skipify-demo/cloudrun_image:${{ env.TAG }}"
region = "us-central1"
account_id = "cloudrun-deidentify-05"
name = "cloudrun-srv-deidentify"
percent = "100"
cpu = "2"
memory = "1024Mi"
type = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
