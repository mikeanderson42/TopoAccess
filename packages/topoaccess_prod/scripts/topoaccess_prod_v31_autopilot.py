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

from topoaccess_prod.harness.benchmark import run_benchmark
from topoaccess_prod.harness.post_edit_validation import run_fixture
from topoaccess_prod.harness.token_accounting import run_token_accounting
from topoaccess_prod.harness.workspace import profile_status
from topoaccess_prod.integrations.tool_schema import write_tool_schema


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--profile", default="default")
    p.add_argument("--cache", default="cache/topoaccess_v21")
    p.add_argument("--release", default="release/topoaccess_prod_v31")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--heartbeat-seconds", type=int, default=30)
    args = p.parse_args()
    Path(args.release).mkdir(parents=True, exist_ok=True)
    state = {
        "workspace": profile_status(args.profile)["status"],
        "tool_schema": bool(write_tool_schema(Path(args.release) / "tool_schema.json")),
        "token_accounting_rows": len(run_token_accounting(["exact_lookup", "change_planning"], "runs/topoaccess_prod_v31/autopilot_token_accounting.jsonl")),
        "agent_benchmark_rows": len(run_benchmark(["codex_style_with_topoaccess"], ["exact_lookup"], 10, 10, "runs/topoaccess_prod_v31/autopilot_agent_benchmark.jsonl")),
        "post_edit_rows": len(run_fixture("tmp/topoaccess_prod_v31_autopilot", "runs/topoaccess_prod_v31/autopilot_post_edit_validation.jsonl")),
        "resume_command": "python packages/topoaccess_prod/scripts/topoaccess_prod_v31_autopilot.py --profile default --cache cache/topoaccess_v21 --release release/topoaccess_prod_v31 --resume --heartbeat-seconds 30",
    }
    path = Path("runs/topoaccess_prod_v31/autopilot_state.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    print(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
