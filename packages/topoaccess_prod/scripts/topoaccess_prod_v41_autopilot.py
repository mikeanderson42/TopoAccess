#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(command, text=True, capture_output=True)
    return {
        "command": " ".join(command),
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-1000:],
        "stderr_tail": completed.stderr[-1000:],
        "result_status": "passed" if completed.returncode == 0 else "failed",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V41 public release polish checklist.")
    parser.add_argument("--profile", default="default")
    parser.add_argument("--release", default="release/topoaccess_prod_v41")
    parser.add_argument("--remote", default="https://github.com/mikeanderson42/TopoAccess.git")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--heartbeat-seconds", type=int, default=30)
    args = parser.parse_args()

    Path(args.release).mkdir(parents=True, exist_ok=True)
    out = Path("runs/topoaccess_prod_v41/autopilot.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    commands = [
        ["python", "-m", "pytest", "packages/topoaccess_prod/tests"],
        ["python", "-m", "compileall", "."],
        ["python", "packages/topoaccess_prod/scripts/topoaccess_conformance_check.py", "--release", args.release],
    ]
    with out.open("a", encoding="utf-8") as handle:
        for command in commands:
            handle.write(json.dumps(run(command)) + "\n")
    print({"autopilot": "complete", "release": args.release, "remote": args.remote})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
