# Live terminal capture — received CloudTrail root-use alert

- **Context:** Phase B test of EventBridge rule and private SQS alert queue, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy python cloud/read_root_alert.py`.
- **Expected:** A test root-use CloudTrail event reaches the queue.
- **Actual:** The script displayed `Messages received: 1`, an AWS CloudTrail API call for `LookupEvents`, and `Identity type: Root`.
- **Interpretation:** One alert was received in SQS. This is **not** email receipt and also confirms root use, which fails the project's no-root criterion.
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). `atl-cloud-GRP01` is a real isolated UTS namespace hostname on physical host `morgoth`, not a project VM.
