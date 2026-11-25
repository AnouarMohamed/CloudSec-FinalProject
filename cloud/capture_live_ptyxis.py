"""Record real commands in Ptyxis and capture the live X11 window.

This runs Ptyxis on a private Xvfb display because GNOME Wayland denies
programmatic desktop screenshots here. The shell uses a real UTS namespace
hostname, atl-cloud-GRP01. No command output is synthesized or edited.
Each PNG is a lossless conversion of the X window's raw XWD pixels.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "cloud/evidence"
BIN = Path("/home/anouar/.local/share/grp01-x11/usr/bin")
LIB = "/home/anouar/.local/share/grp01-x11/usr/lib64"
DISPLAY = ":99"
PROMPT = b"[GRP01] atl-cloud-GRP01"
SESSION = EVIDENCE / "terminal-live" / "ptyxis-live.session"
TITLE = "GRP01 | live terminal evidence"


def run(*args: str, env: dict[str, str] | None = None, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["rtk", "proxy", *args],
        env=env,
        text=True,
        capture_output=True,
        check=True,
        timeout=timeout,
    )


def xdo(*args: str) -> None:
    run("env", f"DISPLAY={DISPLAY}", f"LD_LIBRARY_PATH={LIB}", str(BIN / "xdotool"), *args)


def prompt_count() -> int:
    try:
        return SESSION.read_bytes().count(PROMPT)
    except FileNotFoundError:
        return 0


def wait_prompt(after: int, timeout: int = 90) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if prompt_count() > after:
            time.sleep(0.25)
            return
        time.sleep(0.2)
    raise TimeoutError(f"No shell prompt after command within {timeout}s")


def send(command: str, timeout: int = 90) -> None:
    before = prompt_count()
    xdo("type", "--clearmodifiers", "--delay", "1", command)
    xdo("key", "Return")
    wait_prompt(before, timeout)


def screenshot(window: str, relative: str, label: str) -> None:
    target = EVIDENCE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    xdo("set_window", "--name", f"GRP01 | {label}", window)
    time.sleep(0.3)
    with tempfile.NamedTemporaryFile(suffix=".xwd") as raw:
        run("env", f"DISPLAY={DISPLAY}", str(BIN / "xwd"), "-id", window, "-out", raw.name)
        run("magick", raw.name, str(target))
    print(f"CAPTURE {target.relative_to(ROOT)}", flush=True)


def capture(window: str, relative: str, label: str, commands: list[str], timeout: int = 90) -> None:
    xdo("key", "ctrl+l")
    time.sleep(0.2)
    send("date -u")
    for command in commands:
        send(command, timeout)
    screenshot(window, relative, label)


def wait_window() -> str:
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        result = run("env", f"DISPLAY={DISPLAY}", str(BIN / "xwininfo"), "-root", "-tree")
        match = re.search(r'(0x[0-9a-f]+) "GRP01 \| live terminal evidence"', result.stdout)
        if match:
            return match.group(1)
        time.sleep(0.5)
    raise TimeoutError("Ptyxis window did not appear")


def main() -> None:
    global SESSION
    repair = sys.argv[1:] == ["--repair"]
    repair_pod = sys.argv[1:] == ["--repair-pod"]
    if sys.argv[1:] and not (repair or repair_pod):
        raise SystemExit("Usage: capture_live_ptyxis.py [--repair|--repair-pod]")
    if repair or repair_pod:
        SESSION = EVIDENCE / "terminal-live" / ("ptyxis-repair.session" if repair else "ptyxis-pod.session")
    SESSION.parent.mkdir(parents=True, exist_ok=True)
    if SESSION.exists():
        raise SystemExit(f"Refusing to overwrite {SESSION}")
    shell = ROOT / "cloud/live_ptyxis_shell.sh"
    gui_env = os.environ.copy()
    gui_env.pop("WAYLAND_DISPLAY", None)
    gui_env.update({"DISPLAY": DISPLAY, "GDK_BACKEND": "x11", "GTK_A11Y": "none"})
    log_path = Path("/tmp/grp01-ptyxis-capture.log")
    with log_path.open("w") as log:
        server = subprocess.Popen(
            ["rtk", "proxy", str(BIN / "Xvfb"), DISPLAY, "-ac", "-screen", "0", "1600x1000x24", "-nolisten", "tcp"],
            stdout=log, stderr=subprocess.STDOUT,
        )
        terminal = None
        try:
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                try:
                    run("env", f"DISPLAY={DISPLAY}", str(BIN / "xwininfo"), "-root")
                    break
                except subprocess.CalledProcessError:
                    time.sleep(0.2)
            else:
                raise TimeoutError("Xvfb did not start")
            terminal = subprocess.Popen(
                ["rtk", "proxy", "dbus-run-session", "--", "ptyxis", "--standalone", "-T", TITLE,
                 "--", "script", "-q", "-f", "-c", str(shell), str(SESSION)],
                env=gui_env, stdout=log, stderr=subprocess.STDOUT,
            )
            window = wait_window()
            xdo("windowsize", window, "1500", "900")
            xdo("windowfocus", "--sync", window)
            xdo("key", "--repeat", "2", "--delay", "100", "ctrl+plus")
            wait_prompt(0, 30)

            if repair_pod:
                capture(window, "k8s/terminal-pod-security-final.png", "restricted pod security", [
                    "rtk proxy kubectl -n grp01-demo get deployment grp01-web -o json | jq -c '{pod:.spec.template.spec.securityContext,container:.spec.template.spec.containers[0].securityContext}'",
                    "rtk proxy kubectl -n grp01-demo get deployment grp01-web -o json | jq -c '.spec.template.spec.containers[0].resources'",
                ])
                return

            if repair:
                capture(window, "account/terminal-root-safety.png", "root MFA and keys", [
                    "rtk proxy aws iam get-account-summary --profile cloud --query 'SummaryMap.{RootMFA:AccountMFAEnabled,RootKeys:AccountAccessKeysPresent}' --output json",
                ])
                capture(window, "vpc/terminal-routes-compact.png", "public and private routes", [
                    "rtk proxy aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-0d069fce4ce5ff50a --profile cloud --region eu-west-3 --query 'RouteTables[*].[RouteTableId,Associations[*].SubnetId,Routes[*].[DestinationCidrBlock,GatewayId]]' --output text",
                ])
                capture(window, "iam/terminal-role-trust.png", "scoped role trust", [
                    "rtk proxy aws iam get-role --role-name cloud-app-read-grp01 --profile cloud --query 'Role.AssumeRolePolicyDocument.Statement' --output json",
                ])
                capture(window, "iam/terminal-role-policy.png", "scoped role policy", [
                    "rtk proxy aws iam get-role-policy --role-name cloud-app-read-grp01 --policy-name cloud-app-read-grp01 --profile cloud --query PolicyDocument --output json",
                ])
                capture(window, "k8s/terminal-pod-security-compact.png", "restricted pod security", [
                    "rtk proxy kubectl -n grp01-demo get deployment grp01-web -o json | jq '{pod:.spec.template.spec.securityContext,container:.spec.template.spec.containers[0].securityContext}'",
                    "rtk proxy kubectl -n grp01-demo get deployment grp01-web -o json | jq '.spec.template.spec.containers[0].resources'",
                ])
                capture(window, "cloudtrail/terminal-log-delivery.png", "delivered CloudTrail log object", [
                    "rtk proxy aws s3api list-objects-v2 --bucket cloud-trail-logs-grp01 --prefix AWSLogs/227755136916/CloudTrail/eu-west-3/2026/11/25/ --max-keys 1 --profile cloud --region eu-west-3 --query 'Contents[0].{Key:Key,Size:Size}' --output json",
                ])
                return

            capture(window, "account/terminal-identity.png", "AWS identity and MFA", [
                "hostname",
                "rtk proxy aws sts get-caller-identity --profile cloud",
                "rtk proxy aws iam list-mfa-devices --user-name anouar-admin --profile cloud --query 'MFADevices[*].SerialNumber' --output json",
                "rtk proxy aws iam list-mfa-devices --user-name zakaria-admin --profile cloud --query 'MFADevices[*].SerialNumber' --output json",
            ])
            capture(window, "bucket/terminal-config.png", "private docs bucket", [
                "rtk proxy aws s3api get-public-access-block --bucket cloud-docs-grp01 --profile cloud --region eu-west-3",
                "rtk proxy aws s3api get-bucket-encryption --bucket cloud-docs-grp01 --profile cloud --region eu-west-3 --query 'ServerSideEncryptionConfiguration.Rules[*].ApplyServerSideEncryptionByDefault.SSEAlgorithm' --output json",
                "rtk proxy aws s3api get-bucket-versioning --bucket cloud-docs-grp01 --profile cloud --region eu-west-3",
            ])
            capture(window, "bucket/terminal-anonymous.png", "anonymous S3 refusal", [
                "rtk proxy aws s3api head-bucket --bucket cloud-docs-grp01 --no-sign-request --region eu-west-3",
            ])
            capture(window, "vpc/terminal-segmentation.png", "VPC subnets and Security Groups", [
                "rtk proxy aws ec2 describe-subnets --filters Name=vpc-id,Values=vpc-0d069fce4ce5ff50a --profile cloud --region eu-west-3 --query 'Subnets[*].[SubnetId,CidrBlock,MapPublicIpOnLaunch]' --output table",
                "rtk proxy aws ec2 describe-security-groups --filters Name=vpc-id,Values=vpc-0d069fce4ce5ff50a --profile cloud --region eu-west-3 --query 'SecurityGroups[*].[GroupName,IpPermissions]' --output json",
            ])
            capture(window, "vpc/terminal-routes.png", "VPC routes", [
                "rtk proxy aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-0d069fce4ce5ff50a --profile cloud --region eu-west-3 --query 'RouteTables[*].{Id:RouteTableId,Routes:Routes[*].{Dest:DestinationCidrBlock,Gateway:GatewayId}}' --output json",
            ])
            capture(window, "cloudtrail/terminal-trail.png", "CloudTrail management events", [
                "rtk proxy aws cloudtrail describe-trails --trail-name-list cloud-trail-grp01 --profile cloud --region eu-west-3 --query 'trailList[*].[Name,IsMultiRegionTrail,IncludeGlobalServiceEvents,S3BucketName]' --output table",
                "rtk proxy aws cloudtrail get-event-selectors --trail-name cloud-trail-grp01 --profile cloud --region eu-west-3 --query 'EventSelectors[*].[IncludeManagementEvents,ReadWriteType]' --output table",
                "rtk proxy aws cloudtrail get-trail-status --name cloud-trail-grp01 --profile cloud --region eu-west-3 --query '{Logging:IsLogging,Delivery:LatestDeliveryTime,Error:LatestDeliveryError}'",
            ])
            capture(window, "cloudtrail/terminal-log-bucket.png", "private CloudTrail logs", [
                "rtk proxy aws s3api get-public-access-block --bucket cloud-trail-logs-grp01 --profile cloud --region eu-west-3",
                "rtk proxy aws s3api get-bucket-encryption --bucket cloud-trail-logs-grp01 --profile cloud --region eu-west-3 --query 'ServerSideEncryptionConfiguration.Rules[*].ApplyServerSideEncryptionByDefault.SSEAlgorithm' --output json",
                "rtk proxy aws s3api list-objects-v2 --bucket cloud-trail-logs-grp01 --max-keys 1 --profile cloud --region eu-west-3 --query 'Contents[*].[Key,Size]' --output table",
            ])
            capture(window, "cloudtrail/terminal-alert.png", "received root-use alert", [
                "rtk proxy python cloud/read_root_alert.py",
            ], timeout=45)
            capture(window, "secrets/terminal-retrieval.png", "Secrets Manager retrieval", [
                "rtk proxy python cloud/secret_demo.py get",
            ])
            capture(window, "iam/terminal-scoped-role.png", "scoped workload IAM role", [
                "rtk proxy aws iam get-role --role-name cloud-app-read-grp01 --profile cloud --query 'Role.AssumeRolePolicyDocument' --output json",
                "rtk proxy aws iam get-role-policy --role-name cloud-app-read-grp01 --policy-name cloud-app-read-grp01 --profile cloud --query PolicyDocument --output json",
            ])
            capture(window, "prowler/terminal-comparison.png", "Prowler before and after", [
                "rtk proxy python audit/summarize_prowler.py audit/prowler-initial/grp01-initial.csv",
                "rtk proxy python audit/summarize_prowler.py audit/prowler-final/grp01-final-hardened.csv",
                "rtk proxy python audit/summarize_prowler.py audit/prowler-final/grp01-secret-targeted.csv",
            ])
            capture(window, "budget/terminal-status.png", "budget thresholds and email contact", [
                "rtk proxy aws budgets describe-notifications-for-budget --account-id 227755136916 --budget-name cloud-budget-grp01 --profile cloud --query 'Notifications[*].[Threshold,NotificationType,NotificationState]' --output table",
                "rtk proxy aws notificationscontacts list-email-contacts --profile cloud --region eu-west-3 --query 'emailContacts[*].[name,address,status]' --output table",
            ])
            capture(window, "deny/terminal-refusal.png", "explicit bucket-policy denial", [
                "rtk proxy aws s3api list-objects-v2 --bucket cloud-docs-grp01 --profile cloud --region eu-west-3",
            ])

            pod_ip = run("kubectl", "-n", "grp01-demo", "get", "pod", "-l", "app=grp01-web",
                         "-o", "jsonpath={.items[0].status.podIP}").stdout.strip()
            if not re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", pod_ip):
                raise RuntimeError(f"Unexpected pod IP: {pod_ip!r}")
            capture(window, "k8s/terminal-network.png", "Kubernetes NetworkPolicy test", [
                "rtk proxy kubectl -n grp01-demo get pods -o custom-columns=NAME:.metadata.name,IP:.status.podIP",
                "rtk proxy kubectl -n grp01-demo get networkpolicy",
                f"rtk proxy kubectl -n grp01-demo exec grp01-allowed -- curl --max-time 5 -sS http://{pod_ip}:5678",
                f"rtk proxy kubectl -n grp01-demo exec grp01-blocked -- curl --max-time 5 -sS http://{pod_ip}:5678",
            ])
            capture(window, "k8s/terminal-pod-security.png", "Kubernetes Pod Security", [
                "rtk proxy kubectl -n grp01-demo get deployment grp01-web -o json | jq '.spec.template.spec | {serviceAccountName,automountServiceAccountToken,securityContext,container:(.containers[0] | {securityContext,resources})}'",
            ])
            capture(window, "k8s/terminal-rbac-secret.png", "Kubernetes RBAC and Secret", [
                "rtk proxy kubectl auth can-i get secrets -n grp01-demo --as system:serviceaccount:grp01-demo:grp01-web",
                "rtk proxy kubectl -n grp01-demo get secret grp01-demo-secret -o custom-columns=NAME:.metadata.name,TYPE:.type",
                "rtk proxy kubectl get namespace grp01-demo --show-labels",
            ])
            capture(window, "secrets/terminal-gitleaks.png", "repo and Git history secret scans", [
                "rtk proxy gitleaks dir . --redact --verbose",
                "rtk proxy gitleaks git . --redact --verbose",
            ], timeout=600)
        finally:
            if terminal is not None and terminal.poll() is None:
                try:
                    xdo("type", "exit")
                    xdo("key", "Return")
                    terminal.wait(timeout=8)
                except Exception:
                    terminal.terminate()
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()


if __name__ == "__main__":
    main()
