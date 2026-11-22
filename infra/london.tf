provider "aws" {
  alias  = "london"
  region = "eu-west-2" # United Kingdom: applications from UK customers
}

resource "aws_s3_bucket" "decision_logs_uk" {
  provider = aws.london
  bucket   = "sample-lender-decision-logs-uk"
}
