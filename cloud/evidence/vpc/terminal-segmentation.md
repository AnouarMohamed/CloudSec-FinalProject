# Live terminal capture — VPC subnets and Security Groups

- **Context:** Phase B project VPC `vpc-0d069fce4ce5ff50a` in `eu-west-3`, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws ec2 describe-subnets --filters Name=vpc-id,Values=vpc-0d069fce4ce5ff50a --profile cloud --region eu-west-3 --query 'Subnets[*].[SubnetId,CidrBlock,MapPublicIpOnLaunch]' --output table`; `rtk proxy aws ec2 describe-security-groups --filters Name=vpc-id,Values=vpc-0d069fce4ce5ff50a --profile cloud --region eu-west-3 --query 'SecurityGroups[*].[GroupName,IpPermissions]' --output json`.
- **Expected:** Public/private subnet pair and no public admin-port ingress.
- **Actual:** Subnets `10.71.10.0/24` and `10.71.20.0/24` exist; neither auto-assigns public IPs. All three listed groups have empty ingress permission lists.
- **Interpretation:** No listed project-VPC group permits SSH or RDP ingress from `0.0.0.0/0` or `::/0`. Route classification is shown separately; this query covers this VPC, not the account's other VPCs.
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). `atl-cloud-GRP01` is the real isolated UTS namespace hostname on physical host `morgoth`, not a project VM.
