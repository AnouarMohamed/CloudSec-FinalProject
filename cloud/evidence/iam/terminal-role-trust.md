# Live terminal capture — workload role trust

- **Context:** Phase C project workload role `cloud-app-read-grp01`, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws iam get-role --role-name cloud-app-read-grp01 --profile cloud --query 'Role.AssumeRolePolicyDocument.Statement' --output json`.
- **Expected:** Only a bounded project workload service can assume this example role.
- **Actual:** The trust statement allows `ecs-tasks.amazonaws.com` and requires source account `227755136916` and an ECS ARN in `eu-west-3` for the same account.
- **Interpretation:** The role's trust is scoped to ECS tasks in this account and region. No ECS workload was deployed to exercise it.
- **Method:** Genuine Ptyxis window on private Xvfb, recorded in [ptyxis-repair.session](../terminal-live/ptyxis-repair.session). `atl-cloud-GRP01` is the real hostname inside an isolated UTS namespace on physical host `morgoth`, not a project VM. The window was captured without cropping or retouching.
