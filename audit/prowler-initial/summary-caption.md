# Initial Prowler severity capture

- **Context:** Full initial account scan, parsed from its saved raw CSV on 2026-11-25. `summary.session` is the genuine terminal recording; `summary.png` is a render of that recording with only terminal control characters removed. It shows `[GRP01]`, actual hostname `morgoth`, and the UTC timestamp.
- **Command shown:** `rtk proxy python3 audit/summarize_prowler.py audit/prowler-initial/grp01-initial.csv`, following `date -u`.
- **Expected:** Severity counts calculated from the saved raw findings.
- **Actual:** 670 finding rows, including 351 FAIL: 0 CRITICAL and 113 HIGH. Timestamp `Wed Nov 25 10:32:46 UTC 2026`.
- **Interpretation:** This is the unmodified before baseline. It includes account-wide and pre-existing findings, not only the project resources.
