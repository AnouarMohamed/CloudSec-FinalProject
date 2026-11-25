# Naming checklist annex — GRP01 (draft)

The teacher ID provided was `01`; the required displayed form is `GRP01`, and cloud resource suffix is `grp01`. Names below must be checked against actual inventory before submission.

| Element | Required/chosen name | Associated proof | Status |
|---|---|---|---|
| Web VM and hostname | [WAITING ON TEAMMATE: `atl-web-GRP01`] | [WAITING ON TEAMMATE: VM/terminal capture] | waiting on teammate |
| Directory server VM and hostname | [WAITING ON TEAMMATE: `atl-dc-GRP01`] | [WAITING ON TEAMMATE: VM/terminal capture] | waiting on teammate |
| Database VM and hostname | [WAITING ON TEAMMATE: `atl-db-GRP01`] | [WAITING ON TEAMMATE: VM/terminal capture] | waiting on teammate |
| AD domain | [WAITING ON TEAMMATE: `grp01.atlaslog.local`] | [WAITING ON TEAMMATE: AD configuration] | waiting on teammate |
| TLS certificate DN | [WAITING ON TEAMMATE: CN/FQDN, O=Université Mundiapolis, OU=3ALI-SEC-2627] | [WAITING ON TEAMMATE: certificate output] | waiting on teammate |
| Human AD/system accounts | [WAITING ON TEAMMATE: `prenom.nom` account list] | [WAITING ON TEAMMATE: account listing] | waiting on teammate |
| Current cloud CLI IAM user | `anouar-admin` (real AWS listing; **does not meet** `prenom.nom` convention) | `cloud/evidence/account/identity.txt` [PENDING] | discrepancy |
| Project docs bucket | `cloud-docs-grp01` | `cloud/terraform/baseline.tf` output; `cloud/evidence/bucket/baseline.png` | verified |
| Project cost budget | `cloud-budget-grp01` | `cloud/evidence/budget/notifications.png` | verified |
| Project VPC/subnets/SGs | [PENDING: Terraform output and AWS CLI listing] | `cloud/evidence/vpc/` [PENDING] | missing |
| Project CloudTrail/log bucket | [PENDING: Terraform output and AWS CLI listing] | `cloud/evidence/cloudtrail/` [PENDING] | missing |
| Project IAM roles/policies | [PENDING: Terraform output and AWS CLI listing] | `cloud/evidence/iam/` [PENDING] | missing |

Existing `gridguard` and CloudFormation resources predate this project and are listed separately in the journal; they are not claimed as GRP01 deliverables.
