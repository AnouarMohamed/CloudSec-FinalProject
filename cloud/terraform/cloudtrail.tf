locals {
  trail_name = "cloud-trail-grp01"
  trail_arn  = "arn:aws:cloudtrail:eu-west-3:${data.aws_caller_identity.current.account_id}:trail/${local.trail_name}"
}

resource "aws_s3_bucket" "trail" {
  bucket = "cloud-trail-logs-grp01"
}

resource "aws_s3_bucket_public_access_block" "trail" {
  bucket                  = aws_s3_bucket.trail.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "trail" {
  bucket = aws_s3_bucket.trail.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

data "aws_iam_policy_document" "trail_bucket" {
  statement {
    sid       = "CloudTrailAclCheck"
    effect    = "Allow"
    actions   = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.trail.arn]
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [local.trail_arn]
    }
  }

  statement {
    sid       = "CloudTrailWrite"
    effect    = "Allow"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.trail.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*"]
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [local.trail_arn]
    }
    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }
  }

  statement {
    sid     = "DenyInsecureTransport"
    effect  = "Deny"
    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.trail.arn,
      "${aws_s3_bucket.trail.arn}/*",
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
}

resource "aws_s3_bucket_policy" "trail" {
  bucket     = aws_s3_bucket.trail.id
  policy     = data.aws_iam_policy_document.trail_bucket.json
  depends_on = [aws_s3_bucket_public_access_block.trail]
}

# One multi-Region management-event copy has no CloudTrail event charge.
# S3 log storage and requests can still incur small charges.
resource "aws_cloudtrail" "project" {
  name                          = local.trail_name
  s3_bucket_name                = aws_s3_bucket.trail.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true
  enable_logging                = true
  event_selector {
    read_write_type           = "All"
    include_management_events = true
  }
  depends_on = [aws_s3_bucket_policy.trail, aws_s3_bucket_server_side_encryption_configuration.trail]
}

# Root API activity is a real alert in this user-directed root session.
# The private queue makes delivery testable without waiting for email opt-in.
resource "aws_sqs_queue" "root_alerts" {
  name                      = "cloud-root-alerts-grp01"
  message_retention_seconds = 1209600
  sqs_managed_sse_enabled   = true
}

resource "aws_cloudwatch_event_rule" "root_usage" {
  name        = "cloud-root-usage-grp01"
  description = "Alert on AWS CloudTrail management calls by root"
  # The default ENABLED state excludes read-only management calls such as
  # DescribeVpcs. Include them so a harmless read can prove delivery.
  state = "ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS"
  event_pattern = jsonencode({
    "detail-type" = ["AWS API Call via CloudTrail"]
    detail = {
      userIdentity = {
        type = ["Root"]
      }
    }
  })
}

data "aws_iam_policy_document" "root_alert_queue" {
  statement {
    sid       = "AllowEventBridgeRule"
    effect    = "Allow"
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.root_alerts.arn]
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_cloudwatch_event_rule.root_usage.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "root_alerts" {
  queue_url = aws_sqs_queue.root_alerts.id
  policy    = data.aws_iam_policy_document.root_alert_queue.json
}

resource "aws_cloudwatch_event_target" "root_alerts" {
  rule       = aws_cloudwatch_event_rule.root_usage.name
  target_id  = "cloud-root-alerts-grp01"
  arn        = aws_sqs_queue.root_alerts.arn
  depends_on = [aws_sqs_queue_policy.root_alerts]
}

output "cloudtrail_name" {
  value = aws_cloudtrail.project.name
}

output "root_alert_queue_url" {
  value = aws_sqs_queue.root_alerts.id
}
