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

from topoaccess_prod.harness.prompt_pack_optimizer import optimize
from topoaccess_prod.harness.real_agent_soak import run_soak
from topoaccess_prod.harness.token_ledger import write_ledger
from topoaccess_prod.install.doctor import run_doctor
from topoaccess_prod.install.harness_installer import install_target
from topoaccess_prod.install.workspace_init import validate_workspace


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--profile", default="default")
    p.add_argument("--cache", default="cache/topoaccess_v21")
    p.add_argument("--release", default="release/topoaccess_prod_v32")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--heartbeat-seconds", type=int, default=30)
    args = p.parse_args()
    state = {
        "workspace": validate_workspace(args.profile)["status"],
        "doctor_checks": len(run_doctor(args.profile)),
        "installer_targets": [install_target(t, args.profile, True)["target"] for t in ["codex", "claude-code", "openclaw", "hermes", "generic"]],
        "token_ledger_rows": len(write_ledger(["exact_lookup", "change_planning"], "runs/topoaccess_prod_v32/autopilot_token_ledger.jsonl", "REPORT_topoaccess_prod_v32_token_ledger.md")),
        "prompt_pack_rows": len(optimize(["codex", "claude"], "runs/topoaccess_prod_v32/autopilot_prompt_pack_eval.jsonl", "REPORT_topoaccess_prod_v32_prompt_packs.md")),
        "real_agent_soak_rows": len(run_soak(10, 10, ["codex_with_topoaccess"], "runs/topoaccess_prod_v32/autopilot_real_agent_soak.jsonl", "REPORT_topoaccess_prod_v32_real_agent_soak.md")),
        "resume_command": "python packages/topoaccess_prod/scripts/topoaccess_prod_v32_autopilot.py --profile default --cache cache/topoaccess_v21 --release release/topoaccess_prod_v32 --resume --heartbeat-seconds 30",
    }
    path = Path("runs/topoaccess_prod_v32/autopilot_state.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    print(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
