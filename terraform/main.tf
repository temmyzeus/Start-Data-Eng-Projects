provider "aws" {
  region = var.region
  shared_config_files = var.aws_config_path
  shared_credentials_files = var.aws_credentials_path
  profile = var.profile
}

resource "aws_s3_bucket" "S3-Bucket" {
  bucket_prefix = var.bucket_prefix
  tags = {
    project = "aws_airflow"
  }
}
