"""Create a fictional Kubernetes demo secret without writing its value to disk."""

import secrets
import subprocess


def main() -> None:
    value = secrets.token_urlsafe(24)
    subprocess.run(
        ["kubectl", "create", "secret", "generic", "grp01-demo-secret", "-n", "grp01-demo", "--from-file=value=/dev/stdin"],
        input=value,
        text=True,
        check=True,
    )


if __name__ == "__main__":
    main()
