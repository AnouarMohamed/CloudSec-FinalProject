# Live terminal capture — budget thresholds and email contact

- **Context:** Phase A/D budget review, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws budgets describe-notifications-for-budget --account-id 227755136916 --budget-name cloud-budget-grp01 --profile cloud --query 'Notifications[*].[Threshold,NotificationType,NotificationState]' --output table`; `rtk proxy aws notificationscontacts list-email-contacts --profile cloud --region eu-west-3 --query 'emailContacts[*].[name,address,status]' --output table`.
- **Expected:** Actual-spend notifications at 25, 50, and 100 USD with an active recipient and tested delivery.
- **Actual:** Thresholds `25.0`, `50.0`, and `100.0` show `ACTUAL` and `OK`; `bishopgas4@gmail.com` shows status `inactive`.
- **Interpretation:** Thresholds are configured, but recipient activation and delivered budget email are unproven. `OK` is notification state, not confirmation of email receipt.
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). `atl-cloud-GRP01` is a real isolated UTS namespace hostname on physical host `morgoth`, not a project VM.
