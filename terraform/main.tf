provider "aws" {
  region = var.region
}

resource "aws_kms_key" "this" {
  description             = "dont need this key"
  deletion_window_in_days = 7
  enable_key_rotation     = true
  rotation_period_in_days = 365

  key_usage                = "ENCRYPT_DECRYPT"
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
}

resource "aws_kms_alias" "this" {
  name          = "alias/${var.kms_alias}"
  target_key_id = aws_kms_key.this.key_id
}
