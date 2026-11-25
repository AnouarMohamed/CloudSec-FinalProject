# GRP01 final checklist — 2026-11-25

| Check | Result | Evidence or limit |
|---|---|---|
| Section 0 values | Filled locally in root `AGENTS.md`; no `<<FILL>>` values remain | `AGENTS.md` is Git-ignored by the existing project settings. |
| Project naming and tags | GRP01 cloud resources use `grp01`; Terraform AWS provider supplies `Project=Cloud`, `Group=01`, `Owner=Anouar Mohamed` tags where supported | `audit/report/naming-annex.md`, `cloud/terraform/versions.tf`. Existing `anouar-admin` name and root build identity do not meet the `prenom.nom`/no-root targets. |
| Secrets in repo and history | Gitleaks reported zero findings in the working tree and six then-current commits | `cloud/evidence/secrets/gitleaks.png`; rerun after this evidence-only commit for final history coverage. |
| Ignore rules | Terraform state/plans, tfvars, `.env`, private-key files, provider cache, and generated Prowler compliance exports are ignored | `.gitignore`. |
| Before and after audits | Both raw CSV and OCSF saved; summary and comparison saved | `audit/prowler-initial/`, `audit/prowler-final/`, `cloud/evidence/prowler/`. Initial 0 CRITICAL/113 HIGH; final 0/97 account-wide plus two targeted secret HIGH exceptions. |
| Evidence map and captions | All claimed requirements mapped; each report figure points to a caption and raw terminal session. The PNGs are Freeze renders, not GNOME terminal window screenshots; the real hostname is `morgoth` with a `[GRP01]` prefix. Strict PDF capture compliance remains unmet. | `cloud/evidence/evidence-index.md`, `audit/report/draft.md`, `docs/pdf-gap-review.md`. |
| Budget delivery | Incomplete | Recipient `inactive`; owner must verify email link and wait for a real threshold event. |
| Human MFA and root non-use | Incomplete | `zakaria-admin` lacks MFA: [WAITING ON TEAMMATE: account owner]. User-directed root CLI use prevents a no-root claim. |
| Teardown | Pending explicit approval | `audit/report/teardown-plan.md`; no resource destroyed. |
| PDF deliverables | Incomplete | Architecture dossier and consolidated 15–20 minute defense preparation are absent; audit report remains a draft with teammate placeholders. See `docs/pdf-gap-review.md`. |

This checklist is a draft for Anouar to review before submission.
