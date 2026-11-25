"""Read a real EventBridge SQS alert and print only nonsensitive fields.

The full SQS body is handled in memory because CloudTrail event records include
temporary access key IDs. Nothing is deleted from the queue or saved to disk.
"""

import json
import subprocess


QUEUE = "https://sqs.eu-west-3.amazonaws.com/227755136916/cloud-root-alerts-grp01"


def main() -> None:
    result = subprocess.run(
        [
            "aws", "sqs", "receive-message", "--queue-url", QUEUE,
            "--max-number-of-messages", "1", "--wait-time-seconds", "10",
            "--profile", "cloud", "--region", "eu-west-3", "--output", "json",
        ],
        check=True, capture_output=True, text=True,
    )
    messages = json.loads(result.stdout).get("Messages", [])
    print(f"Messages received: {len(messages)}")
    for message in messages:
        event = json.loads(message["Body"])
        detail = event.get("detail", {})
        print(f"Message ID: {message['MessageId']}")
        print(f"Event time: {event.get('time')}")
        print(f"Event type: {event.get('detail-type')}")
        print(f"Event source: {event.get('source')}")
        print(f"API action: {detail.get('eventName')}")
        print(f"Identity type: {detail.get('userIdentity', {}).get('type')}")
    if not messages:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
