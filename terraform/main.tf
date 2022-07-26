provider "aws" {
  region = var.region
  shared_config_files = var.aws_config_path
  shared_credentials_files = var.aws_credentials_path
  profile = var.profile
}

resource "aws_s3_bucket" "S3-Bucket" {
  bucket_prefix = var.bucket_prefix
  tags = {
    project = "aws_airflow" #edit if this is later used by airflow
  }
}

resource "aws_instance" "airflow_instance" {
  ami = "ami-0d70546e43a941d70" # Ubuntu 22.04
  instance_type = "t2.micro"
  availability_zone = var.AZ
  tags = var.AIRFLOW_TAG
}

resource "aws_ebs_volume" "airflow_instance_volume" {
  availability_zone = var.AZ
  size = 8
  type = "gp2" #general purpose ssd
}

resource "aws_volume_attachment" "airflow_ec2_ebs_attach" {
  device_name = "/dev/sdh"
  volume_id = aws_ebs_volume.airflow_instance_volume.id
  instance_id = aws_instance.airflow_instance.id
  depends_on = [
    aws_instance.airflow_instance,
    aws_ebs_volume.airflow_instance_volume
  ]
}
