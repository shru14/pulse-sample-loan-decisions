provider "aws" {
  region = "eu-west-1" # Ireland: applications from Irish customers
}

resource "aws_s3_bucket" "decision_logs" {
  bucket = "sample-lender-decision-logs-ie"
}

resource "aws_s3_bucket_lifecycle_configuration" "decision_logs" {
  bucket = aws_s3_bucket.decision_logs.id
  rule {
    id     = "keep-400-days"
    status = "Enabled"
    expiration { days = 400 }
  }
}
