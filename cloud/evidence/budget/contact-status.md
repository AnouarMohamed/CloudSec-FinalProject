# Budget email contact status

Context: 2026-11-25 UTC, after sending an AWS activation email for the GRP01 budget recipient.

Command: `aws notificationscontacts list-email-contacts --profile cloud --region eu-west-3 --output json` (run through `rtk proxy`). The image includes the real `date -u` output and the `[GRP01]` prompt.

Expected: `bishopgas4@gmail.com` has an active contact before budget alert delivery can be claimed.

Actual: AWS returned `inactive`. The earlier `send-activation-code` API call returned success, but the recipient has not yet completed activation in the AWS console.

Interpretation: the $25/$50/$100 thresholds are configured; email delivery is not verified. This status may change after the owner confirms the AWS email link. Original session: `contact-status.session`; rendered capture: `contact-status.png`.
