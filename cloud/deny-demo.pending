# Bonus D: a project-scoped equivalent of an SCP denial, without enabling
# Organizations or changing any unrelated account policy.
data "aws_iam_policy_document" "deny_demo_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:PrincipalArn"
      values   = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
  }
}

resource "aws_iam_role" "deny_demo" {
  name               = "cloud-deny-demo-grp01"
  assume_role_policy = data.aws_iam_policy_document.deny_demo_assume.json
}

data "aws_iam_policy_document" "deny_demo" {
  # This allow makes the test meaningful: the explicit Deny below must win.
  statement {
    sid       = "AllowProjectBucketListingForDemonstration"
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.docs.arn]
  }
  statement {
    sid       = "DenyProjectBucketListing"
    effect    = "Deny"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.docs.arn]
  }
}

resource "aws_iam_role_policy" "deny_demo" {
  name   = "cloud-deny-demo-grp01"
  role   = aws_iam_role.deny_demo.id
  policy = data.aws_iam_policy_document.deny_demo.json
}
