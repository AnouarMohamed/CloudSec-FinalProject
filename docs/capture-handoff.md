# GRP01 capture handoff (draft)

The 20 current-state PNGs below are genuine, unretouched screenshots of a live Ptyxis terminal window. Each shows `date -u`, the `[GRP01]` prompt, the exact command and its full visible output. The commands were recorded in [three raw sessions](../cloud/evidence/terminal-live/README.md); every PNG has an adjacent caption with context, expected and actual results, and limitations. Ptyxis ran on a private Xvfb display with a real `atl-cloud-GRP01` hostname inside an isolated UTS namespace. The physical host remained `morgoth`, and this environment was not a project VM.

| Phase | Generated PNGs |
|---|---|
| A | [Current identity and MFA](../cloud/evidence/account/terminal-identity.png), [root MFA and keys](../cloud/evidence/account/terminal-root-safety.png), [budget thresholds and contact](../cloud/evidence/budget/terminal-status.png) |
| B | [Docs bucket configuration](../cloud/evidence/bucket/terminal-config.png), [anonymous refusal](../cloud/evidence/bucket/terminal-anonymous.png), [subnets and Security Groups](../cloud/evidence/vpc/terminal-segmentation.png), [route tables](../cloud/evidence/vpc/terminal-routes-compact.png), [trail status](../cloud/evidence/cloudtrail/terminal-trail.png), [log bucket configuration](../cloud/evidence/cloudtrail/terminal-log-bucket.png), [delivered log object](../cloud/evidence/cloudtrail/terminal-log-delivery.png), [received root-use alert](../cloud/evidence/cloudtrail/terminal-alert.png) |
| C | [Secret retrieval](../cloud/evidence/secrets/terminal-retrieval.png), [role trust](../cloud/evidence/iam/terminal-role-trust.png), [role policy](../cloud/evidence/iam/terminal-role-policy.png), [Prowler comparison](../cloud/evidence/prowler/terminal-comparison.png), [working-tree and history Gitleaks](../cloud/evidence/secrets/terminal-gitleaks.png) |
| D | [Explicit bucket-policy refusal](../cloud/evidence/deny/terminal-refusal.png) |
| F | [Allowed and blocked network traffic](../cloud/evidence/k8s/terminal-network.png), [Pod Security and resource limits](../cloud/evidence/k8s/terminal-pod-security-final.png), [RBAC and Secret metadata](../cloud/evidence/k8s/terminal-rbac-secret.png) |

The historical Phase A bucket image [baseline.png](../cloud/evidence/bucket/baseline.png) is a Freeze rendering of the original recorded session, **not** a live terminal-window screenshot. The original [session](../cloud/evidence/bucket/baseline.session), before-state Git commit `6bcbecc`, and [initial raw Prowler report](../audit/prowler-initial/grp01-initial.csv) remain available. The before state cannot be rerun after hardening.

## Captures still needed by hand

1. **Budget email activation and real delivery.** Activate the AWS User Notifications contact for `bishopgas4@gmail.com` through the verification email while signed into this account. Once active, capture the contact status in a terminal using:

   ```bash
   date -u
   aws notificationscontacts list-email-contacts --profile cloud --region eu-west-3 --query 'emailContacts[*].[name,address,status]' --output table
   ```

   Save the genuine AWS email alert only when a configured threshold is naturally crossed. The current contact is `inactive`; no delivered budget email is claimed. Do not incur spend just to make this image.

2. **Strict project-VM hostname presentation, if the teacher requires it.** The current captures show the group hostname in an isolated namespace. On an actual group-named project VM, use its GNOME terminal and capture a real session with:

   ```bash
   export PS1='[GRP01] \h\$ '
   date -u
   hostname
   aws sts get-caller-identity --profile cloud
   aws s3api head-bucket --bucket cloud-docs-grp01 --no-sign-request --region eu-west-3
   ```

   Use a non-root IAM `cloud` profile on that VM. Its CLI identity must be checked honestly; the current workstation profile is root and cannot satisfy the no-root rubric. If the VM is not available, retain the disclosed capture-environment limitation.

3. **Teammate-owned figures.** `[WAITING ON TEAMMATE: network/VPN and Suricata, Lynis before/after, LUKS and restore tests, VM isolation, PingCastle and BloodHound, AD and certificate naming proofs.]` Each teammate must supply the exact command/configuration, timestamp, full real output, and result before their figure can be completed. No output or screenshot has been invented for these parts.

The no-root-ever criterion cannot be repaired with a later screenshot: this project used the root CLI profile on 2026-11-25 at the user's explicit direction, and the received CloudTrail alert proves a root event occurred. The final Prowler scan also still has HIGH findings; see [comparison](../audit/prowler-final/comparison.md).
