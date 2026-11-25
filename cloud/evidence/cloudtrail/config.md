# CloudTrail configuration capture

- **Context:** Phase B trail `cloud-trail-grp01` after Terraform apply on 2026-11-25. `config.session` is the real terminal recording; `config.png` renders the full visible content with `[GRP01]`, hostname `morgoth`, and UTC time.
- **Commands shown:** `rtk proxy aws cloudtrail describe-trails --trail-name-list cloud-trail-grp01 --profile cloud --region eu-west-3 --query 'trailList[0].{Name:Name,MultiRegion:IsMultiRegionTrail,Global:IncludeGlobalServiceEvents,Validation:LogFileValidationEnabled,Bucket:S3BucketName}'`; `get-trail-status`; `get-event-selectors`; `rtk proxy aws s3api get-public-access-block --bucket cloud-trail-logs-grp01 --profile cloud`; `get-bucket-encryption`, following `date -u`.
- **Expected:** Active multi-Region trail, all management events, encrypted private dedicated bucket.
- **Actual:** `IsLogging: true`, `MultiRegion: true`, global events and log-file validation true, event selector `ReadWriteType: All`/`IncludeManagementEvents: true`; all four bucket public access blocks true; `AES256`. At `Wed Nov 25 10:37:12 UTC 2026`, `LatestDeliveryTime` was still null immediately after creation.
- **Interpretation:** Configuration is correct, but this capture alone does not prove log delivery or alert receipt. Follow-up delivery and alert tests are required.
