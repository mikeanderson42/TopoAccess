#!/usr/bin/env python
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
for path in [ROOT, REPO]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from topoaccess_prod.cli.topoaccessctl import run_command


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--cache", default="cache/topoaccess_v21")
    p.add_argument("--release", default="release/topoaccess_prod")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--heartbeat-seconds", type=int, default=30)
    a = p.parse_args()
    state = {
        "status": run_command("status", a.cache, a.release)["status"],
        "self_check": run_command("self-check", a.cache, a.release)["status"],
        "field_trial": run_command("field-trial", a.cache, a.release, requests=1000, fallback_requests=1000)["status"],
        "release": run_command("validate-release", a.cache, a.release)["status"],
        "resume_command": "python packages/topoaccess_prod/scripts/topoaccess_prod_autopilot.py --cache cache/topoaccess_v21 --release release/topoaccess_prod --resume --heartbeat-seconds 30",
    }
    path = Path("runs/topoaccess_prod/autopilot_state.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    print(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
