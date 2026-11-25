# Terraform manages metadata only. The secret value is uploaded separately
# from a process-memory pipe, so it never appears in state or Git.
resource "aws_secretsmanager_secret" "app" {
  name                    = "cloud-app-secret-grp01"
  description             = "Fictional AtlasLog application demo secret for GRP01"
  recovery_window_in_days = 7
}

# The secret accepts reads only from the project's workload role. The role's
# identity policy also limits its read access to this one secret.
data "aws_iam_policy_document" "app_secret" {
  statement {
    sid       = "AllowProjectWorkloadRead"
    effect    = "Allow"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [aws_secretsmanager_secret.app.arn]
    principals {
      type        = "AWS"
      identifiers = [aws_iam_role.app_read.arn]
    }
  }
}

resource "aws_secretsmanager_secret_policy" "app" {
  secret_arn          = aws_secretsmanager_secret.app.arn
  policy              = data.aws_iam_policy_document.app_secret.json
  block_public_policy = true
}

data "aws_iam_policy_document" "app_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = ["arn:aws:ecs:eu-west-3:${data.aws_caller_identity.current.account_id}:*"]
    }
  }
}

# This is a scoped example ECS task role. No ECS task is launched, so it
# demonstrates policy design without running compute or claiming active use.
resource "aws_iam_role" "app_read" {
  name               = "cloud-app-read-grp01"
  assume_role_policy = data.aws_iam_policy_document.app_assume.json
}

data "aws_iam_policy_document" "app_read" {
  statement {
    sid       = "ReadProjectDocuments"
    effect    = "Allow"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.docs.arn}/*"]
  }
  statement {
    sid       = "ReadProjectSecret"
    effect    = "Allow"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [aws_secretsmanager_secret.app.arn]
  }
}

resource "aws_iam_role_policy" "app_read" {
  name   = "cloud-app-read-grp01"
  role   = aws_iam_role.app_read.id
  policy = data.aws_iam_policy_document.app_read.json
}

output "app_secret_arn" {
  value = aws_secretsmanager_secret.app.arn
}

output "app_read_role_arn" {
  value = aws_iam_role.app_read.arn
}
