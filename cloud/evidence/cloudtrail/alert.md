# Received root-use alert capture

- **Context:** EventBridge/SQS alert delivery test after enabling read-only management-event matching on 2026-11-25. `alert.session` is the genuine terminal recording; `alert.png` is the complete render with `[GRP01]`, real hostname `morgoth`, and UTC timestamp. The reader script prints selected nonsensitive fields from the real SQS message in memory; the underlying CloudTrail body contains a temporary access-key ID and is intentionally not saved or printed.
- **Commands shown:** `rtk proxy aws ec2 describe-vpcs --vpc-ids vpc-0d069fce4ce5ff50a --profile cloud --region eu-west-3 --query 'Vpcs[].VpcId'` and `rtk proxy python3 cloud/read_root_alert.py`, following `date -u`.
- **Expected:** A genuine root management API call appears in the queue targeted by `cloud-root-usage-grp01`.
- **Actual:** One message received, ID `5b4127ef-ce71-4473-b875-9c55fb8c36cf`, event time `2026-11-25T10:44:25Z`, `AWS API Call via CloudTrail`, action `LookupEvents`, identity type `Root`. Capture timestamp `Wed Nov 25 10:46:35 UTC 2026`.
- **Interpretation:** The alert was triggered and received for a real earlier `LookupEvents` call made during the test. The `DescribeVpcs` command shown in the same capture was a separate root management call; it is not claimed as the source of this particular message. SQS rather than email is the tested delivery channel.
