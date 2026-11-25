# Naming checklist annex — GRP01 (draft)

The teacher ID provided was `01`; the required displayed form is `GRP01`, and cloud resource suffix is `grp01`. Cloud names below were checked against Terraform output and the cited CLI evidence; teammate names remain proposals awaiting their proof.

| Element | Required/chosen name | Associated proof | Status |
|---|---|---|---|
| Web VM and hostname | [WAITING ON TEAMMATE: `atl-web-GRP01`] | [WAITING ON TEAMMATE: VM/terminal capture] | waiting on teammate |
| Directory server VM and hostname | [WAITING ON TEAMMATE: `atl-dc-GRP01`] | [WAITING ON TEAMMATE: VM/terminal capture] | waiting on teammate |
| Database VM and hostname | [WAITING ON TEAMMATE: `atl-db-GRP01`] | [WAITING ON TEAMMATE: VM/terminal capture] | waiting on teammate |
| AD domain | [WAITING ON TEAMMATE: `grp01.atlaslog.local`] | [WAITING ON TEAMMATE: AD configuration] | waiting on teammate |
| TLS certificate DN | [WAITING ON TEAMMATE: CN/FQDN, O=Université Mundiapolis, OU=3ALI-SEC-2627] | [WAITING ON TEAMMATE: certificate output] | waiting on teammate |
| Human AD/system accounts | [WAITING ON TEAMMATE: `prenom.nom` account list] | [WAITING ON TEAMMATE: account listing] | waiting on teammate |
| Current cloud CLI IAM user | `anouar-admin` initially, then root (real STS results; **neither meets** the intended final `prenom.nom` least-privilege identity) | `cloud/evidence/account/identity.png`, `cloud/evidence/account/root-identity.png` | discrepancy |
| Project docs bucket | `cloud-docs-grp01` | `cloud/terraform/baseline.tf`; `cloud/evidence/bucket/hardened.png` | verified |
| Project cost budget | `cloud-budget-grp01` | `cloud/evidence/budget/notifications.png` | verified |
| Project VPC/subnets/SGs/NACL | `cloud-vpc-grp01`; `cloud-subnet-public-grp01`; `cloud-subnet-private-grp01`; `cloud-sg-public-grp01`; `cloud-sg-private-grp01`; `cloud-sg-default-grp01`; `cloud-acl-default-grp01` | `cloud/evidence/vpc/segmentation.png`, `cloud/evidence/vpc/routes.png`, `cloud/evidence/iam/remediation.png`, `cloud/terraform/vpc.tf` | verified |
| Project CloudTrail/log bucket and alert | `cloud-trail-grp01`; `cloud-trail-logs-grp01`; `cloud-root-usage-grp01`; `cloud-root-alerts-grp01` | `cloud/evidence/cloudtrail/config.png`, `cloud/evidence/cloudtrail/delivery.png`, `cloud/evidence/cloudtrail/alert.png` | verified |
| Project application secret and workload role/policy | `cloud-app-secret-grp01`; `cloud-app-read-grp01` | `cloud/evidence/secrets/retrieval.png`, `cloud/evidence/iam/scoped-role.png` | verified |
| Project deny demonstration role/policy and bucket statement | `cloud-deny-demo-grp01`; `DenyProjectBucketListingForDemonstration` on `cloud-docs-grp01` | `cloud/terraform/deny-demo.tf`, `cloud/evidence/deny/refusal.png` | role created; bucket denial tested; root cannot assume role |
| Local Kubernetes cluster, namespace, workloads and policies | `grp01`; `grp01-demo`; `grp01-web`; `grp01-allowed`; `grp01-blocked`; `grp01-default-deny`; `grp01-allow-web`; `grp01-allow-client` | `cloud/evidence/k8s/network-policy.png`, `cloud/evidence/k8s/hardening.png` | verified locally |

Existing `gridguard` and CloudFormation resources predate this project and are listed separately in the journal; they are not claimed as GRP01 deliverables.
