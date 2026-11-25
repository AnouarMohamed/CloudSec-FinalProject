data "aws_caller_identity" "current" {}

# S3 already encrypts new objects by default. Managing this rule explicitly
# makes the required control visible and reproducible in Terraform.
resource "aws_s3_bucket_server_side_encryption_configuration" "docs" {
  bucket = aws_s3_bucket.docs.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "docs" {
  bucket = aws_s3_bucket.docs.id
  versioning_configuration {
    status = "Enabled"
  }
}

data "aws_iam_policy_document" "docs_bucket" {
  # Bonus D: deny a harmless read action even for an otherwise authorized
  # principal. The bucket is empty; PutBucketPolicy remains available so the
  # policy can be revised by Terraform after the demonstration.
  statement {
    sid       = "DenyProjectBucketListingForDemonstration"
    effect    = "Deny"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.docs.arn]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
  }

  statement {
    sid     = "DenyInsecureTransport"
    effect  = "Deny"
    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.docs.arn,
      "${aws_s3_bucket.docs.arn}/*",
    ]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
    condition {
      test     = "Bool"
      variable = "aws:PrincipalIsAWSService"
      values   = ["false"]
    }
  }

  # Explicitly reject outsiders, including anonymous requests. The block
  # public access settings separately prevent accidental public grants.
  statement {
    sid     = "DenyOtherAccounts"
    effect  = "Deny"
    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.docs.arn,
      "${aws_s3_bucket.docs.arn}/*",
    ]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "StringNotEquals"
      variable = "aws:PrincipalAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
    condition {
      test     = "Bool"
      variable = "aws:PrincipalIsAWSService"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "docs" {
  bucket     = aws_s3_bucket.docs.id
  policy     = data.aws_iam_policy_document.docs_bucket.json
  depends_on = [aws_s3_bucket_public_access_block.docs]
}
