# GRP01 Prowler HIGH/CRITICAL before and after

Counts are failed finding rows in the full account scans, not project-only scores. Raw CSV/OCSF files are retained in `audit/prowler-initial/` and `audit/prowler-final/`. The table groups rows by check ID; inspect the raw reports for individual resource IDs.

**Failed CRITICAL/HIGH rows:** before 0/113; after 0/97.

| Finding/check | Severity | Before | After | Fix or explanation | Status |
|---|---|---:|---:|---|---|
| `cloudtrail_multi_region_enabled` | HIGH | 17 | 0 | Added multi-Region management trail (`cloud/terraform/cloudtrail.tf`). | absent after |
| `cloudwatch_log_group_data_protection_policy_configured` | HIGH | 6 | 6 | Existing account resource or global check outside GRP01; no change made. | open |
| `config_delegated_admin_and_org_aggregator_all_regions` | HIGH | 1 | 1 | Existing account resource or global check outside GRP01; no change made. | open |
| `ec2_ebs_default_encryption` | HIGH | 1 | 1 | Existing account resource or global check outside GRP01; no change made. | open |
| `ec2_ebs_volume_encryption` | HIGH | 1 | 1 | Existing account resource or global check outside GRP01; no change made. | open |
| `ec2_ebs_volume_snapshots_exists` | HIGH | 1 | 1 | Existing account resource or global check outside GRP01; no change made. | open |
| `ec2_instance_account_imdsv2_enabled` | HIGH | 1 | 1 | Existing account resource or global check outside GRP01; no change made. | open |
| `ec2_networkacl_allow_ingress_any_port` | HIGH | 3 | 4 | Project default NACL `acl-01ce0f4ca6b243df6` changed to deny-only; other account NACL findings remain (see raw resource IDs). | open |
| `ec2_securitygroup_allow_ingress_from_internet_to_any_port` | HIGH | 1 | 1 | Existing account resource or global check outside GRP01; no change made. | open |
| `ec2_securitygroup_allow_ingress_from_internet_to_tcp_port_22` | HIGH | 1 | 1 | Existing account resource or global check outside GRP01; no change made. | open |
| `ecr_repository_image_no_secrets` | HIGH | 4 | 4 | Existing account resource or global check outside GRP01; no change made. | open |
| `iam_avoid_root_usage` | HIGH | 1 | 1 | User-directed root session; historical use cannot be undone. | open |
| `iam_policy_allows_privilege_escalation` | HIGH | 2 | 2 | Existing account resource or global check outside GRP01; no change made. | open |
| `iam_role_cross_service_confused_deputy_prevention` | HIGH | 2 | 2 | Project role trust now requires `aws:SourceAccount`; two pre-existing roles remain outside GRP01. | open |
| `iam_user_hardware_mfa_enabled` | HIGH | 1 | 1 | Existing `zakaria-admin`; [WAITING ON TEAMMATE: account owner to register MFA]. | open |
| `iam_user_mfa_enabled_console_access` | HIGH | 1 | 1 | Existing `zakaria-admin`; [WAITING ON TEAMMATE: account owner to register MFA]. | open |
| `s3_bucket_shadow_resource_vulnerability` | HIGH | 68 | 68 | No GRP01 bucket implicated; finding persists in the final account scan without a direct project fix. | open |
| `vpc_subnet_no_public_ip_by_default` | HIGH | 1 | 1 | Existing account resource or global check outside GRP01; no change made. | open |
