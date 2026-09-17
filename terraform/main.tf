terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" { region = var.aws_region }

resource "aws_s3_bucket" "feature_store" {
  bucket = "${var.environment}-ml-feature-store-${var.aws_account_id}"
  tags = { Environment = var.environment, Component = "FeatureStore" }
}

resource "aws_dynamodb_table" "online_feature_store" {
  name           = "${var.environment}_online_features"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "entity_id"

  attribute {
    name = "entity_id"
    type = "S"
  }
}
