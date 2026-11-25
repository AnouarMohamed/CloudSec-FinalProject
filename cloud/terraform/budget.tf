# The free notification-only budget tracks gross monthly spend; its three
# percentage thresholds correspond to 25, 50, and 100 USD.
resource "aws_budgets_budget" "project" {
  name         = "cloud-budget-grp01"
  budget_type  = "COST"
  limit_amount = "100"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    notification_type          = "ACTUAL"
    threshold                  = 25
    threshold_type             = "PERCENTAGE"
    subscriber_email_addresses = ["bishopgas4@gmail.com"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    notification_type          = "ACTUAL"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    subscriber_email_addresses = ["bishopgas4@gmail.com"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    notification_type          = "ACTUAL"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    subscriber_email_addresses = ["bishopgas4@gmail.com"]
  }
}
