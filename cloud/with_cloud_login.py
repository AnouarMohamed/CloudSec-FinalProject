"""Run a child process with temporary credentials from the cloud CLI profile.

AWS CLI browser login is supported by the CLI but not yet by every SDK. This
launcher reads the CLI's process-format export into memory, passes it only to
the child environment, and never writes or prints credential values.
"""

import json
import os
import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: with_cloud_login.py COMMAND [ARGS ...]", file=sys.stderr)
        return 2

    result = subprocess.run(
        ["aws", "configure", "export-credentials", "--profile", "cloud", "--format", "process"],
        check=True,
        capture_output=True,
        text=True,
    )
    credentials = json.loads(result.stdout)
    environment = os.environ.copy()
    for source, destination in (
        ("AccessKeyId", "AWS_ACCESS_KEY_ID"),
        ("SecretAccessKey", "AWS_SECRET_ACCESS_KEY"),
        ("SessionToken", "AWS_SESSION_TOKEN"),
    ):
        value = credentials.get(source)
        if not value:
            raise RuntimeError(f"AWS CLI did not supply {source}")
        environment[destination] = value
    environment["AWS_REGION"] = "eu-west-3"
    environment["AWS_DEFAULT_REGION"] = "eu-west-3"
    environment.pop("AWS_PROFILE", None)

    os.execvpe(sys.argv[1], sys.argv[1:], environment)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
