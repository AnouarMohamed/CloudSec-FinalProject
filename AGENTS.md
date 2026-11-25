# AGENTS.md: Cloud, Audit and Kubernetes workstream (integrator project)

## 0. Fill these in before starting (the agent must refuse to proceed if any is still a placeholder)

- GROUP_ID: `01` (display label `GRP01`; lowercase resource suffix `grp01`)
- CLOUD_PROVIDER: `AWS`
- CLOUD_REGION: `eu-west-3` (Paris). Use this region for everything unless a service is unavailable there; ask me before using another.
- AWS_PROFILE: `cloud` (an IAM user with AdministratorAccess and MFA, NOT the root account; see rule 2)
- ALERT_EMAIL: `bishopgas4@gmail.com`
- STUDENT_NAME: `Anouar Mohamed`
- BUDGET: the account has about 116 USD of credits (user-reported on 2026-11-25). Budget alert thresholds: 25, 50 and 100 USD.

At the very start, ask me for any value still written as `<<FILL: ...>>` in ONE message, wait for my answer, write the values into this file, then continue. Never guess or invent an identifier, especially GROUP_ID.

## 1. Who I am and what this is

I am a student on a university security project (Université Mundiapolis, module "Sécurité des infrastructures et Cloud"), in a group of 4. We secure a fictional SME, AtlasLog, end to end. **My workstream is: cloud (AWS/Azure free tier), the audit report, and the optional Kubernetes bonus (Bonus A).** My teammates own network/VPN, Linux systems/data, and Active Directory/identity. You are my assistant for my workstream only.

The work is graded and defended live. I may be asked individual questions about everything you build. Your job is to make me faster **while keeping me able to explain and reproduce every piece.**

## 2. Hard rules (never violate, even if I ask casually)

1. **Scope.** Only touch my own cloud account, my own local files, and this repo. Never scan, probe or attack any third-party system, other groups' resources, or the university network. Audit tools (Prowler, etc.) run only against my own account.
2. **Credentials.** Use only the profile in AWS_PROFILE, which is an IAM admin user so you can build everything without permission blockers. Never use or request the AWS **root account** credentials: the spec requires proof that root is never used, and root access keys are a serious risk. If a task seems to need root (very rare, for example closing the account or some billing settings), stop and tell me what to do manually. Never write access keys, secrets, tokens, passwords or private keys into any file in the repo, shell history, logs, Terraform state committed to Git, or the report. Secrets go in Secrets Manager or environment variables only. Add `.gitignore` entries for `*.tfstate*`, `.terraform/`, `*.tfvars` with secrets, `.env`, `*.pem`, `*.key` before the first commit.
3. **Cost.** The account has about 116 USD of credits (user-reported on 2026-11-25), so small, short-lived costs are acceptable, but credits are not unlimited and the spec says to stay within free-tier limits where possible. Prefer free-tier options. Before creating anything that costs money, tell me the estimated cost and wait for approval. At the start, verify the budget alerts exist (see BUDGET). Always ask first for NAT gateways, load balancers, managed Kubernetes control planes (EKS), EC2 beyond free tier, and anything that runs continuously. Use local k3s/kind for the Kubernetes bonus. Destroy temporary billable resources as soon as the evidence is captured. List anything billable that still exists when we finish.
4. **Naming (graded, non-negotiable).** Every cloud resource name must contain the group ID, for example `cloud-docs-<grpnn>`, `cloud-vpc-<grpnn>`, `cloud-trail-<grpnn>`, IAM roles/policies like `cloud-<purpose>-<grpnn>`. Any user or account is named `prenom.nom`. No generic names (`admin1`, `test`, `my-bucket`). Tag every taggable resource with `Project=Cloud`, `Group=<GROUP_ID>`, `Owner=<STUDENT_NAME>`.
5. **Fictional data only.** Never store real personal data in any bucket, database or repo.
6. **Honesty about evidence.** Never fabricate, edit, paraphrase or "reconstruct" command output, scores, findings or screenshots. If something was not run, say so. If a command fails, show the real error. Evidence in the report must come from real runs I performed or approved.
7. **Autonomy and limits.** I am short on time, so work autonomously and keep going without asking for routine, non-billable, reversible steps: you may run `terraform apply` for changes that match the requirements in this file, after you check the plan yourself. Show me a short summary of each apply afterwards. Still stop and ask before: `terraform destroy`, deleting buckets or data that hold evidence, anything billable above the approved level, anything that exposes a resource publicly, changes to the account itself (Organizations, SCPs, MFA, root), and anything irreversible outside this project.
8. **Do not ask me to disable security controls** (MFA, encryption, logging) to make something work. Fix the root cause.

## 3. How to work with me (so I can defend it)

- Work in small steps. Before each step: one or two sentences on **what** and **why**. After each step: what changed and how to verify it.
- Prefer Terraform for infrastructure so everything is reproducible, reviewable and rebuildable. Run `terraform fmt`, `validate` and `plan`, review the plan yourself, apply, then give me a short summary of what changed (see rule 7 for what still needs my approval).
- Explain every non-obvious setting (for example why a bucket policy denies non-TLS, why a Security Group rule is scoped as it is) in a comment or in a short note I can read. Write notes in plain English; I will rewrite them in my own words.
- Maintain `docs/journal.md`: one dated entry per work session with decisions, incidents, commands of note, and time spent (a journal is required by the spec). Draft entries for me; I confirm them.
- Keep one directory layout:
  - `cloud/terraform/` infrastructure
  - `cloud/evidence/` raw outputs and screenshots index, one subfolder per requirement
  - `audit/` Prowler reports (before/after), comparison tables, checklist
  - `k8s/` Kubernetes bonus
  - `docs/` journal, notes, report drafts
- When you need a decision (region, naming detail, trade-off), ask one clear question with a recommended default instead of guessing.

## 4. Requirements to implement (exact acceptance criteria from the spec)

### Phase A: Baseline first (do this BEFORE hardening)

The project expects a before/after audit, so the starting state must be real and documented.

1. Confirm account safety: root has MFA and is not used; the `cloud` IAM admin user has MFA; billing alerts exist.
2. Create a **deliberately imperfect but safe baseline** (for example a bucket without default encryption/versioning, a Security Group that is too broad but not exposing real data, CloudTrail not yet configured). Ask me before making anything publicly exposed; prefer misconfigurations that Prowler flags without real exposure. Contain no real data. Document exactly what was made imperfect and why in `audit/baseline.md`.
3. Run **Prowler** (initial). Save the raw output to `audit/prowler-initial/` plus a summary table of findings by severity. Tell me the counts of CRITICAL and HIGH.
4. Commit this as the "before" state. Do not overwrite it later.

### Phase B: Cloud socle (mandatory; a part without a complete socle scores 0)

- **Bucket** `cloud-docs-<grpnn>`: private (block all public access), default encryption enabled, versioning on, restrictive bucket policy (deny non-TLS, deny public principals). Acceptance: a public/anonymous access attempt is refused. Evidence: AWS CLI output showing the refusal plus the bucket configuration.
- **VPC** with public and private subnets and restrictive Security Groups. Acceptance: no Security Group allows 0.0.0.0/0 (or ::/0) on admin ports (SSH 22, RDP 3389). Evidence: Security Group listings.
- **CloudTrail** (Azure: equivalent Activity Log) enabled for all management events, delivering to a dedicated log bucket that is also private and encrypted, with at least one alert (for example console login without MFA, root usage, or IAM policy change) that is **actually triggered by a test** and received. Evidence: configuration plus the alert received.

For each item: apply with Terraform, verify with CLI commands, store raw output under `cloud/evidence/<requirement>/` with a timestamp and a short description (context, command shown, expected result, actual result, interpretation).

### Phase C: Challenge level (needed for a good grade)

- **Secrets externalized**: store an application secret in Secrets Manager (or secure environment variables), demonstrate retrieval, and run a secrets scan (gitleaks or trufflehog) across the **entire repo including Git history** showing zero findings. Evidence: retrieval demo and scan output.
- **Prowler full audit with remediation**: remediate all CRITICAL and HIGH findings from the initial report (target: zero), re-run Prowler, save to `audit/prowler-final/`, and produce a before/after comparison table (finding, severity, fix applied, Terraform file or command, status). For anything not remediated, record a justified reason.
- **IAM least privilege (cloud part, shared with the identity teammate; coordinate and do not contradict them)**: no root usage, MFA on all human users, roles scoped to least privilege, no hard-coded access keys anywhere in the code or repo. Evidence: IAM screenshots/CLI output plus the secrets scan. Because the build profile is an admin user, the **final state** must still show least privilege: create scoped roles/policies for the project's workloads and users, remove any unneeded broad permissions and unused access keys, and produce evidence that the root account was not used (CloudTrail query for root events returning nothing). Document that the admin user is a build-time account and what replaced it.

### Phase D: Bonus level (only after socle and challenge are solid)

- Budget and billing alert tested; a Service Control Policy or equivalent that denies at least one unauthorized action, with evidence of the refusal (note: SCPs require AWS Organizations; ask me before enabling it).

### Phase E: Audit report workstream

Build the audit report skeleton (`audit/report/`), structured per course part (1 to 6): state before, state after, measures applied, verifiable evidence. For each part, leave clearly marked placeholders `[WAITING ON TEAMMATE: <what>]` for evidence owned by others (Lynis before/after, PingCastle and BloodHound exports, Suricata alerts, LUKS proof, etc.). Never invent their results.
- Create the **naming checklist annex**: table of VM names, hostnames, AD domain, certificates, accounts, cloud resources, with the chosen name and the associated proof. Fill in the cloud rows from real resource listings (`terraform output`, CLI).
- Every figure or capture in the report needs a caption: context, command or configuration shown, expected result, actual result, interpretation.
- Cite sources (official docs, CIS benchmarks) for anything reused. All text is a draft for me to review and rewrite.

### Phase F: Kubernetes bonus (Bonus A), only if Phases B and C are complete

- Use a **local** distribution (k3s, kind or minikube) to avoid cloud cost. Ask me before any managed-cluster option.
- Deploy a simple sample web app with: NetworkPolicies (default deny, then explicit allows), RBAC with least privilege (dedicated ServiceAccounts, no cluster-admin for workloads), Pod Security (non-root, read-only root filesystem, dropped capabilities, no privileged), resource limits, and secrets handled properly (not committed in plain text).
- Optionally scan with kube-bench, kube-linter or trivy and document before/after.
- Document each hardening measure and the reason for it in `k8s/README.md`, with evidence of the effect (for example a blocked connection that a NetworkPolicy denies).

## 5. Evidence rules (from the spec)

- Terminal captures must show the group hostname and be readable without zoom. Remind me to run commands in a terminal whose prompt shows the group-named hostname, and to take screenshots myself when a visual capture is required. You prepare the command, the expected result and the caption; I perform the capture.
- Anonymous captures (no context, no hostname, no explanation) are forbidden.

### Agent-generated captures (allowed, with these conditions)

I allow you to produce the captures yourself so I save time. They must be genuine:
- Capture only real terminal sessions that you actually ran in this project. Record the session (for example with `script` or asciinema) and render it to a PNG (for example with `freeze`, `termshot` or a headless terminal renderer). If a tool is missing, tell me what to install; do not substitute a mock-up.
- Every capture must show, in the image itself: the prompt with GROUP_ID as a visible prefix (set `PS1` to start with `[<GROUP_ID>]`; this is a label, never fake the real hostname, and never edit it afterwards), the exact command, the full real output, and the real date and time (run `date -u` in the session).
- Never edit, crop out, redact or retouch output in a way that changes its meaning. Redact only secrets (account keys, tokens) and say that you redacted them. Account IDs may be partially masked.
- For AWS console views, prefer CLI evidence. Only use browser automation if it works without storing my password or MFA codes anywhere; otherwise list the console screenshots for me to take by hand.
- Save each capture in `cloud/evidence/<requirement>/` with a `.md` caption beside it: context, command, expected result, actual result, interpretation. Add it to the evidence index.
- Be honest in the final summary about which captures you generated and which I must still take by hand, so I can disclose how they were produced if my teacher asks.
- Every claimed requirement needs a proof file in `cloud/evidence/` and a line in an `evidence-index.md` mapping requirement -> acceptance criterion -> proof file -> status (done / partial / missing).

## 6. Order of work and checkpoints

Work in the order A -> B -> C -> E (continuous) -> D -> F. At the end of each phase:
1. Show a short status table (requirement, status, evidence file).
2. List anything unfinished or risky.
3. Ask me before moving on.

## 7. Teardown and final checks

At the end: list all billable or running resources, propose a teardown plan (the spec requires cutting or deleting billable resources once the project ends), and wait for my approval before destroying anything. Before delivery run a final checklist: naming compliance, no secrets in repo or history, evidence index complete, Prowler before/after both saved, `.gitignore` correct.

## 8. If unsure

If a requirement is ambiguous, a command could cost money or expose data, or a choice affects my teammates (network plan, IAM, naming), stop and ask. When in doubt, choose the safer, cheaper, more reversible option and tell me why.
