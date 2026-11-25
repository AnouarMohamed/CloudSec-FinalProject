# Live terminal capture — CloudTrail status and management events

- **Context:** Phase B trail `cloud-trail-grp01`, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws cloudtrail describe-trails --trail-name-list cloud-trail-grp01 --profile cloud --region eu-west-3 --query 'trailList[*].[Name,IsMultiRegionTrail,IncludeGlobalServiceEvents,S3BucketName]' --output table`; `rtk proxy aws cloudtrail get-event-selectors --trail-name cloud-trail-grp01 --profile cloud --region eu-west-3 --query 'EventSelectors[*].[IncludeManagementEvents,ReadWriteType]' --output table`; `rtk proxy aws cloudtrail get-trail-status --name cloud-trail-grp01 --profile cloud --region eu-west-3 --query '{Logging:IsLogging,Delivery:LatestDeliveryTime,Error:LatestDeliveryError}'`.
- **Expected:** Multi-Region trail, all management events, logging active, delivery without error.
- **Actual:** Multi-Region and global-service flags are `True`; management events are included with `ReadWriteType=All`; logging is `true`, delivery time is populated, and delivery error is `null`.
- **Interpretation:** Configuration and recent delivery status meet the CloudTrail setup check. Received alert is shown separately in [terminal-alert.png](terminal-alert.png).
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). `atl-cloud-GRP01` is a real isolated UTS namespace hostname on physical host `morgoth`, not a project VM.
