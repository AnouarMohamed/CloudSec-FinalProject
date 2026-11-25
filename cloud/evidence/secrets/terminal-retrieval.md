# Live terminal capture — application secret retrieval

- **Context:** Phase C Secrets Manager demo, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy python cloud/secret_demo.py get`.
- **Expected:** The project secret is retrieved successfully without printing its value.
- **Actual:** The script printed the project secret ARN, version ID, and `Retrieval succeeded: 43 characters (value withheld)`.
- **Interpretation:** Retrieval worked at the time of capture. The secret value was suppressed by the demo script, not edited out of the PNG; this does not prove rotation or a running application consumer.
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). `atl-cloud-GRP01` is a real isolated UTS namespace hostname on physical host `morgoth`, not a project VM.
