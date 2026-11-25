"""Count Prowler CSV findings by status and severity without changing evidence."""

import csv
import sys
from collections import Counter


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: summarize_prowler.py REPORT.csv")
    with open(sys.argv[1], newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source, delimiter=";"))
    counts = Counter((row["STATUS"], row["SEVERITY"].upper()) for row in rows)
    print(f"Report: {sys.argv[1]}")
    print(f"Finding rows: {len(rows)}")
    print("Status       CRITICAL  HIGH  MEDIUM  LOW  TOTAL")
    for status in ("FAIL", "PASS", "MANUAL"):
        values = [counts[status, severity] for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW")]
        print(f"{status:<12} {values[0]:>8} {values[1]:>5} {values[2]:>7} {values[3]:>4} {sum(values):>6}")


if __name__ == "__main__":
    main()
