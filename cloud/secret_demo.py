"""Create or retrieve the fictional demo secret without exposing its value.

The generated value is passed to AWS CLI on stdin. No shell argument, log,
Terraform state, or repository file contains the value.
"""

import json
import secrets
import subprocess
import sys


SECRET_ID = "cloud-app-secret-grp01"
BASE = ["aws", "secretsmanager"]
COMMON = ["--profile", "cloud", "--region", "eu-west-3", "--output", "json"]


def main() -> None:
    if sys.argv[1:] == ["put"]:
        value = secrets.token_urlsafe(32)
        command = BASE + [
            "put-secret-value", "--secret-id", SECRET_ID,
            "--secret-string", "file:///dev/stdin",
        ] + COMMON
        result = subprocess.run(command, input=value, capture_output=True, text=True, check=True)
        receipt = json.loads(result.stdout)
        print(f"Secret ID: {receipt['ARN']}")
        print(f"Version ID: {receipt['VersionId']}")
        print("Generated value sent to Secrets Manager from process memory.")
    elif sys.argv[1:] == ["get"]:
        command = BASE + ["get-secret-value", "--secret-id", SECRET_ID] + COMMON
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        response = json.loads(result.stdout)
        value = response.get("SecretString")
        if not value:
            raise RuntimeError("SecretString was absent or empty")
        print(f"Secret ID: {response['ARN']}")
        print(f"Version ID: {response['VersionId']}")
        print(f"Retrieval succeeded: {len(value)} characters (value withheld)")
    else:
        raise SystemExit("usage: secret_demo.py put|get")


if __name__ == "__main__":
    main()
