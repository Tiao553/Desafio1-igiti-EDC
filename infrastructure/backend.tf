# Backend configuration require a AWS storage bucket.
terraform {
  backend "s3" {
    bucket = "sebastiao-igti-backend-tf-531477333755"
    key    = "state/terraform.tfstate"
    region = "us-east-2"
  }
}
