# Baseline: keep the empty project bucket private while omitting explicit
# encryption configuration and versioning. AWS still applies SSE-S3 to new
# objects automatically. Phase B will add explicit settings after the audit.
resource "aws_s3_bucket" "docs" {
  bucket = "cloud-docs-grp01"
}

resource "aws_s3_bucket_public_access_block" "docs" {
  bucket                  = aws_s3_bucket.docs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "docs_bucket_name" {
  value = aws_s3_bucket.docs.bucket
}
