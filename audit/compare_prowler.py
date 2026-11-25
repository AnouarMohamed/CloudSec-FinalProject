"""Generate an honest before/after HIGH/CRITICAL check table from raw CSVs."""

import csv
import sys
from collections import Counter


ACTIONS = {
    "cloudtrail_multi_region_enabled": "Added multi-Region management trail (`cloud/terraform/cloudtrail.tf`).",
    "ec2_networkacl_allow_ingress_any_port": "Project default NACL `acl-01ce0f4ca6b243df6` changed to deny-only; other account NACL findings remain (see raw resource IDs).",
    "iam_role_cross_service_confused_deputy_prevention": "Project role trust now requires `aws:SourceAccount`; two pre-existing roles remain outside GRP01.",
    "iam_avoid_root_usage": "User-directed root session; historical use cannot be undone.",
    "iam_user_hardware_mfa_enabled": "Existing `zakaria-admin`; [WAITING ON TEAMMATE: account owner to register MFA].",
    "iam_user_mfa_enabled_console_access": "Existing `zakaria-admin`; [WAITING ON TEAMMATE: account owner to register MFA].",
    "s3_account_level_public_access_blocks": "Account-level control; rule 7 approval needed, project buckets have all bucket-level blocks.",
    "s3_bucket_shadow_resource_vulnerability": "No GRP01 bucket implicated; absent in after scan without a direct project fix.",
    "secretsmanager_automatic_rotation_enabled": "Fictional demo secret with no consumer; rotation needs a Lambda implementation and is recorded as an exception.",
    "secretsmanager_has_restrictive_resource_policy": "Added role-scoped resource policy with `block_public_policy=true` (`cloud/terraform/secrets-iam.tf`).",
}


def load(path: str) -> tuple[Counter, dict]:
    counts: Counter = Counter()
    examples: dict = {}
    with open(path, newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source, delimiter=";"):
            if row["STATUS"] != "FAIL" or row["SEVERITY"].upper() not in ("CRITICAL", "HIGH"):
                continue
            key = (row["CHECK_ID"], row["SEVERITY"].upper())
            counts[key] += 1
            examples.setdefault(key, row)
    return counts, examples


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: compare_prowler.py BEFORE.csv AFTER.csv")
    before, before_examples = load(sys.argv[1])
    after, after_examples = load(sys.argv[2])
    print("# GRP01 Prowler HIGH/CRITICAL before and after\n")
    print("Counts are failed finding rows in the full account scans, not project-only scores. Raw CSV/OCSF files are retained in `audit/prowler-initial/` and `audit/prowler-final/`. The table groups rows by check ID; inspect the raw reports for individual resource IDs.\n")
    print(f"**Failed CRITICAL/HIGH rows:** before {sum(v for (k,s),v in before.items() if s=='CRITICAL')}/{sum(v for (k,s),v in before.items() if s=='HIGH')}; after {sum(v for (k,s),v in after.items() if s=='CRITICAL')}/{sum(v for (k,s),v in after.items() if s=='HIGH')}.\n")
    print("| Finding/check | Severity | Before | After | Fix or explanation | Status |")
    print("|---|---|---:|---:|---|---|")
    for key in sorted(set(before) | set(after)):
        check, severity = key
        b, a = before[key], after[key]
        row = after_examples.get(key) or before_examples.get(key)
        resource = row["RESOURCE_UID"]
        if check in ACTIONS:
            action = ACTIONS[check]
        elif "grp01" in resource.lower():
            action = f"GRP01 resource `{resource}`; needs project review."
        else:
            action = "Existing account resource or global check outside GRP01; no change made."
        status = "absent after" if b and not a else "new" if not b and a else "open" if a else "none"
        print(f"| `{check}` | {severity} | {b} | {a} | {action} | {status} |")


if __name__ == "__main__":
    main()
