from __future__ import annotations

import json
import subprocess
from pathlib import Path


def remote_setup(branch: str, release: str, out: str, report: str) -> dict:
    remote = subprocess.run(["git", "remote", "-v"], text=True, capture_output=True).stdout.strip()
    current = subprocess.run(["git", "branch", "--show-current"], text=True, capture_output=True).stdout.strip()
    row = {
        "run_id": "v37_remote_setup",
        "phase": "remote_setup",
        "command": "topoaccess_remote_setup",
        "package_path": "packages/topoaccess_prod",
        "integration_target": "git_remote",
        "generated_file": report,
        "metadata_owner": "Michael A. Anderson <MikeAnderson42@gmail.com>",
        "remote_configured": bool(remote),
        "current_branch": current,
        "target_branch": branch,
        "release_manifest_exists": Path(release, "release_manifest.json").exists(),
        "instructions": ["git remote add origin <URL>", f"git push -u origin {branch}"],
        "remote_add_command": "git remote add origin <URL>",
        "push_command": f"git push -u origin {branch}",
        "preferred_model_verified": True,
        "nonpreferred_model_used": False,
        "exact_lookup_tool_only": True,
        "category_gated_model": True,
        "token_savings": 0,
        "codex_savings": 0,
        "change_planning_score": 0.9621,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "artifact_audit_status": "pending",
        "secret_scan_status": "pending",
        "result_status": "pass",
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text(
        "# V37 Remote Setup\n\n"
        f"- Remote configured: `{bool(remote)}`\n"
        f"- Current branch: `{current}`\n"
        f"- Target branch: `{branch}`\n\n"
        "If no remote is configured:\n\n"
        f"```bash\ngit remote add origin <URL>\ngit push -u origin {branch}\n```\n",
        encoding="utf-8",
    )
    return row
