# Secrets Manager upload and retrieval capture

- **Context:** Phase C fictional application secret on 2026-11-25. `retrieval.session` is the actual terminal recording; `retrieval.png` renders the complete visible commands and output with `[GRP01]`, real hostname `morgoth`, and UTC timestamp. The value was generated in memory, sent to AWS CLI on stdin, and never printed or stored in Terraform state or Git.
- **Commands shown:** `rtk proxy python3 cloud/secret_demo.py put` and `rtk proxy python3 cloud/secret_demo.py get`, following `date -u`.
- **Expected:** A secret version created and then retrieved without disclosing the value.
- **Actual:** Both calls report the same ARN and version ID `c18431b8-3204-44e6-8b07-7512e9c39295`; retrieval succeeded for 43 characters, value withheld. Capture timestamp `Wed Nov 25 10:54:25 UTC 2026`.
- **Interpretation:** The application secret is external to code and was retrieved successfully. This does not prove automatic rotation or a running application integration.
