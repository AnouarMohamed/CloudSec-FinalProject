# Initial Prowler severity capture

Context: full 2026-11-25 initial account scan, summarized from `audit/prowler-initial/grp01-initial.csv`. These files are exact copies of the genuine original `audit/prowler-initial/summary.session` and `summary.png`; no output or pixels were edited.

Command shown: `rtk proxy python3 audit/summarize_prowler.py audit/prowler-initial/grp01-initial.csv`, following `date -u` under the `[GRP01]` prompt.

Expected: computed severity counts from the preserved raw report.

Actual: 670 finding rows, 351 FAIL including 0 CRITICAL and 113 HIGH.

Interpretation: account-wide before scan; it includes resources outside GRP01 and is not a project-only score.
