terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 7.0"
    }
  }
}

provider "aws" {
  profile = "cloud"
  region  = "eu-west-3"

  default_tags {
    tags = {
      Project = "Cloud"
      Group   = "01"
      Owner   = "Anouar Mohamed"
    }
  }
}
