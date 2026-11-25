# Initial Prowler account audit — GRP01

Full AWS scan finished on 2026-11-25 with Prowler 5.52.0. Source of truth: `grp01-initial.csv` and `grp01-initial.ocsf.json`. The generated framework-specific `compliance/` exports remain on local disk but are excluded from Git because they add about 70 MB and duplicate the findings in the raw CSV/OCSF files. The first direct-profile attempt failed; `prowler.log` preserves that error. The successful scan used `cloud/with_cloud_login.py` to pass temporary CLI login credentials in process memory.

| Result | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---|---:|---:|---:|---:|---:|
| FAIL | 0 | 113 | 121 | 117 | 351 |
| PASS | 61 | 83 | 150 | 15 | 309 |
| MANUAL | 3 | 1 | 6 | 0 | 10 |

Prowler's displayed completion line said 676 checks; the raw CSV contains 670 finding rows. These count different things, so the severity table is computed from the raw CSV. Prowler exited with status 3 because findings were present, after saving the output.

The 113 HIGH failed rows include 68 `s3_bucket_shadow_resource_vulnerability` reports for globally named service buckets in many regions, 17 regional `cloudtrail_multi_region_enabled` reports, and 6 CloudWatch log-group data-protection reports. Other HIGH findings include pre-existing resources and users outside this project's Terraform state: an internet-open SSH rule on `launch-wizard-1` in `us-east-1`, `zakaria-admin` console MFA disabled, two `gridguard` policies with privilege-escalation actions, and broad network ACLs. Root use is also flagged, following the user's explicit change of plan. These findings need individual remediation or a documented exception; they are not evidence that all 113 are in project resources.
