variable "region_id" {
  default = "us-east-2"
}

variable "prefix" {
  default = "Sebastiao-igti"
}

variable "account" {
  default = 531477333755
}

variable "key_pair_name" {
  default = "sebastiao-igti-teste"
}

variable "airflow_subnet_id" {
  default = "subnet-4cef5427"
}

variable "vpc_id" {
  default = "vpc-d724b4bc"
}

# Prefix configuration and project common tags
locals {
  prefix = "${var.prefix}-${terraform.workspace}"
  common_tags = {
    Project     = "Challenger-igti-module1"
    ManagedBy   = "Terraform"
    Owner       = "Data Engineering"
    Billing     = "Infrastructure"
    Environment = terraform.workspace
    UserEmail   = "sebastiao553@gmail.com"
  }
}

variable "bucket_names" {
  description = "Create S3 buckets with these names"
  type        = list(string)
  default = [
    "landing-zone",
    "processing-zone",
    "delivery-zone"
  ]
}

variable "database_names" {
  description = "Create databases with these names"
  type        = list(string)
  default = [
    #landing-zone
    "dl_landing_zone",
    "dl_processing_zone",
    "dl_delivery_zone"
  ]
}

variable "bucket_paths" {
  description = "Paths to S3 bucket used by the crawler"
  type        = list(string)
  default = [
    "s3://landing-zone-531477333755",
    "s3://processing-zone-531477333755",
    "s3://delivery-zone-531477333755"
  ]
}

variable "bucket_functions" {
  description = "Create S3 bucket for lambda functions"
  default     = "temp-functions-sebastiao-igti"
}