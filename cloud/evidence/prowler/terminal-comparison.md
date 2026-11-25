# Live terminal capture — Prowler before and after counts

- **Context:** Phase A/C audit report comparison, displayed from saved raw CSV files on 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy python audit/summarize_prowler.py audit/prowler-initial/grp01-initial.csv`; `rtk proxy python audit/summarize_prowler.py audit/prowler-final/grp01-final-hardened.csv`; `rtk proxy python audit/summarize_prowler.py audit/prowler-final/grp01-secret-targeted.csv`.
- **Expected:** Real initial/final severity counts, with zero CRITICAL/HIGH target after remediation.
- **Actual:** Initial FAIL rows: 0 CRITICAL, 113 HIGH. Final full-scan FAIL rows: 0 CRITICAL, 97 HIGH. Supplemental project-secret scan: 0 CRITICAL, 2 HIGH.
- **Interpretation:** The screenshot displays real summaries of historical Prowler CSVs; it is not a fresh Prowler run or a screenshot from the initial audit date. The zero-HIGH target remains unmet.
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). `atl-cloud-GRP01` is a real isolated UTS namespace hostname on physical host `morgoth`, not a project VM.
