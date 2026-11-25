"""Render a recorded `script` session without changing its terminal content.

Only terminal control sequences, carriage returns, and script's recording
metadata are removed. The original .session file remains the raw evidence.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: render_session.py SOURCE.session OUTPUT.png")
    source = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
    source = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", source)
    lines = source.replace("\r\n", "\n").replace("\r", "").splitlines()
    lines = [line for line in lines if not line.startswith(("Script started on ", "Script done on "))]
    # The first command is just setting the visible prompt. The prompt and all
    # subsequent commands, timestamps and outputs are retained as recorded.
    while lines and not lines[0].startswith("[GRP01]"):
        lines.pop(0)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".txt") as normalized:
        normalized.write("\n".join(lines).rstrip() + "\n")
        normalized.flush()
        subprocess.run(
            ["freeze", normalized.name, "-o", sys.argv[2], "--width", "1500", "--font.size", "19", "--padding", "30", "--margin", "0"],
            check=True,
        )


if __name__ == "__main__":
    main()
