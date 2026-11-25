# VPC subnet and Security Group capture

- **Context:** Phase B project VPC `vpc-0d069fce4ce5ff50a` on 2026-11-25. `segmentation.session` is the real terminal recording; `segmentation.png` is its complete render with `[GRP01]`, actual hostname `morgoth`, and UTC time.
- **Commands shown:** `rtk proxy aws ec2 describe-subnets --filters Name=vpc-id,Values=vpc-0d069fce4ce5ff50a --profile cloud --region eu-west-3 --query 'Subnets[].{Id:SubnetId,Cidr:CidrBlock,PublicIp:MapPublicIpOnLaunch,Name:Tags[?Key==`Name`].Value|[0]}'` and `rtk proxy aws ec2 describe-security-groups --filters Name=vpc-id,Values=vpc-0d069fce4ce5ff50a --profile cloud --region eu-west-3 --query 'SecurityGroups[].{Name:GroupName,Id:GroupId,Ingress:IpPermissions,Egress:IpPermissionsEgress}'`, following `date -u`.
- **Expected:** Public/private subnets; no project Security Group allows SSH/RDP or internet ingress.
- **Actual:** `10.71.10.0/24` and `10.71.20.0/24`, neither assigning a public IP automatically. All three project VPC Security Groups have `Ingress: []`; the two named groups allow only TCP 443 egress inside `10.71.0.0/16`. Timestamp `Wed Nov 25 10:36:26 UTC 2026`.
- **Interpretation:** No Security Group in the new project VPC allows 0.0.0.0/0 or ::/0 on 22 or 3389. This does not remediate the unrelated us-east-1 `launch-wizard-1` group found by Prowler.

`routes.session`/`routes.png` show the public subnet's `0.0.0.0/0` route to the project internet gateway and the private subnet's local-only route at `Wed Nov 25 10:36:51 UTC 2026`. The expected and actual results match, confirming the subnet roles.
