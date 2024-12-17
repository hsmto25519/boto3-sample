variable "region" {
  default = "ap-northeast-1"
}

variable "kms_alias" {
  description = "Alias name for my KMS key"
  default     = "kms-verification-key"
}
