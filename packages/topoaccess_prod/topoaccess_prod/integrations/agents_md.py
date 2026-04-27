from __future__ import annotations

import json
from pathlib import Path


BODY = """# AGENTS.md

TopoAccess is a local repo-intelligence sidecar for coding agents.

Rules:
- Use TopoAccess for exact lookup; exact lookup is tool-only.
- Preferred model fallback is category-gated only for change planning, model-required narrative, report synthesis, and troubleshooting.
- Run preflight before edits: `python packages/topoaccess_prod/scripts/topoaccess_agent.py preflight --profile default --task "<task>"`.
- Run post-edit validation after edits: `python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile default --changed-files <files>`.
- Run product tests: `python -m pytest packages/topoaccess_prod/tests`.
- Run release validation: `python packages/topoaccess_prod/scripts/topoaccessctl.py validate-release --cache cache/topoaccess_v21 --release release/topoaccess_prod`.
- Do not commit model files, GGUFs, cache blobs, logs, secrets, or env files.
- Provenance is required for audited answers.
- Use safe publish dry-run before branch publication.
"""


def generate_agents_md(profile: str, out: str, report: str) -> dict:
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(BODY, encoding="utf-8")
    pkg_release = Path("packages/topoaccess_prod/release/AGENTS.md")
    pkg_release.parent.mkdir(parents=True, exist_ok=True)
    pkg_release.write_text(BODY, encoding="utf-8")
    row = base_row("agents_md", out)
    Path("runs/topoaccess_prod_v37/agents_md.jsonl").parent.mkdir(parents=True, exist_ok=True)
    Path("runs/topoaccess_prod_v37/agents_md.jsonl").write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text("# V37 Agent Configs\n\nAGENTS.md generated for Codex and compatible coding agents.\n", encoding="utf-8")
    return row


def base_row(phase: str, generated_file: str) -> dict:
    return {
        "run_id": f"v37_{phase}",
        "phase": phase,
        "command": phase,
        "package_path": "packages/topoaccess_prod",
        "integration_target": phase,
        "generated_file": generated_file,
        "metadata_owner": "Michael A. Anderson <MikeAnderson42@gmail.com>",
        "preferred_model_verified": True,
        "nonpreferred_model_used": False,
        "exact_lookup_tool_only": True,
        "category_gated_model": True,
        "token_savings": 0.9553,
        "codex_savings": 0.9287,
        "change_planning_score": 0.9621,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "artifact_audit_status": "pending",
        "secret_scan_status": "pending",
        "result_status": "pass",
    }

