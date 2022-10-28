terraform {
  required_version = ">= 0.12"
  backend "s3" {
    bucket = "terraform-state-files-409021554022"
    key = "start_data_eng_projects/begineer_batch/terraform.tfstate"
    region = "us-west-2"
  }
  required_providers {
    aws = {
      version = ">= 4.23.0"
      source  = "hashicorp/aws"
    }
    local = {
      version = ">= 2.2.3"
      source  = "hashicorp/local"
    }
    tls = {
      version = ">= 4.0.1"
      source  = "hashicorp/tls"
    }
  }
}

provider "aws" {
  region                   = var.region
  shared_config_files      = var.aws_config_path
  shared_credentials_files = var.aws_credentials_path
  profile                  = var.profile
}
