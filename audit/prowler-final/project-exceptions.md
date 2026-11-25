# Project exceptions in the final audit

The full after scan (`grp01-final-hardened.csv`) found 0 CRITICAL and 97 HIGH FAIL rows, compared with 0 and 113 initially. It did not enumerate the GRP01 Secrets Manager secret. A supplemental scan with `--scan-unused-services` (`grp01-secret-targeted.csv`) found two project HIGH failures:

| Check | Current control and evidence | Remaining reason | Status |
|---|---|---|---|
| `secretsmanager_automatic_rotation_enabled` | The fictional secret is retrieved by `cloud/secret_demo.py`; no workload consumes it. | Rotation requires a rotation implementation and a consumer test. No Lambda or continuously running service was created for a demonstration value. | Open, justified exception. |
| `secretsmanager_has_restrictive_resource_policy` | `cloud/terraform/secrets-iam.tf` grants `GetSecretValue` only to `cloud-app-read-grp01`; `block_public_policy=true`. See `cloud/evidence/iam/remediation-final.png`. | Prowler 5.52.0 requires a resource-policy `Deny` on all `secretsmanager:*` actions with an exception for a named IAM principal. With the current root build identity, such a deny could prevent management and recovery of the project secret. The narrower Allow plus public-policy block remains active. | Open, justified exception; do not claim a Prowler pass. |

The initial scan's 68 S3 shadow-resource HIGH rows are still present in the final full scan; none identifies a GRP01 bucket. Additional HIGH rows refer to existing account resources or human users outside this project. Root use occurred at the user's explicit direction and is an unresolved grading failure. `zakaria-admin` has no MFA in the observed listing; [WAITING ON TEAMMATE: that user's owner to enroll MFA].

Raw reports remain unchanged. This table is an interpretation of them, not an edited result.
