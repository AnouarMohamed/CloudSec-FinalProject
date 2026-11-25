"""Test a real denied S3 operation with temporary role credentials in memory."""

import json
import os
import subprocess


ROLE = "arn:aws:iam::227755136916:role/cloud-deny-demo-grp01"


def main() -> None:
    assume = subprocess.run(
        ["aws", "sts", "assume-role", "--role-arn", ROLE,
         "--role-session-name", "grp01-deny-test", "--profile", "cloud", "--output", "json"],
        check=True, capture_output=True, text=True,
    )
    credentials = json.loads(assume.stdout)["Credentials"]
    environment = os.environ.copy()
    for source, destination in (
        ("AccessKeyId", "AWS_ACCESS_KEY_ID"),
        ("SecretAccessKey", "AWS_SECRET_ACCESS_KEY"),
        ("SessionToken", "AWS_SESSION_TOKEN"),
    ):
        environment[destination] = credentials[source]
    environment.pop("AWS_PROFILE", None)
    result = subprocess.run(
        ["aws", "s3api", "list-objects-v2", "--bucket", "cloud-docs-grp01",
         "--region", "eu-west-3", "--output", "json"],
        env=environment, capture_output=True, text=True,
    )
    print(f"Assumed role: {ROLE}")
    print("Attempted: aws s3api list-objects-v2 --bucket cloud-docs-grp01 --region eu-west-3")
    print(f"Exit code: {result.returncode}")
    print(result.stderr.strip() or result.stdout.strip())
    if result.returncode == 0 or "AccessDenied" not in result.stderr:
        raise SystemExit("Expected AccessDenied was not observed")


if __name__ == "__main__":
    main()
