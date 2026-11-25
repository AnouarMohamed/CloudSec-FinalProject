# Live terminal capture — delivered CloudTrail log object

- **Context:** Phase B dedicated log bucket `cloud-trail-logs-grp01`, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws s3api list-objects-v2 --bucket cloud-trail-logs-grp01 --prefix AWSLogs/227755136916/CloudTrail/eu-west-3/2026/11/25/ --max-keys 1 --profile cloud --region eu-west-3 --query 'Contents[0].{Key:Key,Size:Size}' --output json`.
- **Expected:** At least one nonempty `.json.gz` CloudTrail log object is present.
- **Actual:** AWS returned a `.json.gz` key under the `CloudTrail/eu-west-3/2026/11/25/` prefix with size `1928` bytes.
- **Interpretation:** A nonzero compressed log object was delivered. The separate [terminal-log-bucket.png](terminal-log-bucket.png) shows privacy and encryption settings; this listing alone does not validate every event inside the file.
- **Method:** Genuine Ptyxis window on private Xvfb, recorded in [ptyxis-repair.session](../terminal-live/ptyxis-repair.session). `atl-cloud-GRP01` is the real hostname inside an isolated UTS namespace on physical host `morgoth`, not a project VM. The window was captured without cropping or retouching.
