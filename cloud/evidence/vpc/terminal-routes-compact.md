# Live terminal capture — public and private route tables

- **Context:** Phase B project VPC `vpc-0d069fce4ce5ff50a` route check, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-0d069fce4ce5ff50a --profile cloud --region eu-west-3 --query 'RouteTables[*].[RouteTableId,Associations[*].SubnetId,Routes[*].[DestinationCidrBlock,GatewayId]]' --output text`.
- **Expected:** Public subnet associated with an Internet Gateway route; private subnet has only the VPC-local route.
- **Actual:** Private subnet `subnet-0408ffd741f2dd27f` is associated with `rtb-095e1141cfb105807`, which lists only `10.71.0.0/16 local`. Public subnet `subnet-0d5373cc76702fa34` is associated with `rtb-0a64bf31d6fa6cecb`, which lists `0.0.0.0/0` through `igw-0157c4fbe0c31b717` as well as the local route. A third main route table shows only the local route.
- **Interpretation:** The association and routes distinguish project public/private subnets; this does not test packet reachability.
- **Method:** Genuine Ptyxis window on private Xvfb, recorded in [ptyxis-repair.session](../terminal-live/ptyxis-repair.session). `atl-cloud-GRP01` is the real hostname inside an isolated UTS namespace on physical host `morgoth`, not a project VM. The window was captured without cropping or retouching.
