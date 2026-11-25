# Final Prowler counts

Context: GRP01 full-account after scan and a supplemental scan of the GRP01 secret, recorded on 2026-11-25 UTC. The original terminal transcript is `final-summary.session`; `final-summary.png` is an unedited rendering.

Commands: `python audit/summarize_prowler.py audit/prowler-final/grp01-final-hardened.csv` and `python audit/summarize_prowler.py audit/prowler-final/grp01-secret-targeted.csv`, as shown with the `[GRP01]` prompt and `date -u`.

Expected: no CRITICAL or HIGH failures after remediation. Actual: the full account scan has 0 CRITICAL and 97 HIGH FAIL rows (initial: 0 and 113). The supplemental secret scan has 2 HIGH FAIL rows for the project secret. The full scan did not enumerate that secret, so its 97 must not be described as complete project coverage.

Interpretation: the zero-HIGH target is unmet. `audit/prowler-final/comparison.md` maps the full-scan findings; `audit/prowler-final/project-exceptions.md` records the targeted secret findings and limits.
