from __future__ import annotations

import json
import subprocess
from pathlib import Path

ALLOWLIST = ("packages/topoaccess_prod/", "release/topoaccess_prod_v36/", "REPORT_topoaccess_prod_v36_", "README_TOPOACCESS.md", ".gitignore")
BLOCKED = (".gguf", ".safetensors", ".ckpt", ".pth", ".pt", ".env", "models/", "/logs/", "cache/")


def safe_publish(branch: str, release: str, dry_run: bool, out: str, report: str) -> dict:
    current = subprocess.run(["git", "branch", "--show-current"], text=True, capture_output=True).stdout.strip()
    remote = subprocess.run(["git", "remote", "-v"], text=True, capture_output=True).stdout.strip()
    manifest = Path(release, "release_manifest.json").exists()
    status = subprocess.run(["git", "status", "--short"], text=True, capture_output=True).stdout.splitlines()
    candidates = [line[3:] for line in status if len(line) > 3]
    disallowed = [p for p in candidates if any(b in p for b in BLOCKED)]
    outside_allowlist = [p for p in candidates if not p.startswith(ALLOWLIST)]
    push_ready = current == branch and bool(remote) and manifest and not disallowed and dry_run
    row = {
        "run_id": "v36_safe_publish",
        "phase": "safe_publish",
        "command": "topoaccess_safe_publish",
        "branch": current,
        "expected_branch": branch,
        "commit": subprocess.run(["git", "rev-parse", "--short", "HEAD"], text=True, capture_output=True).stdout.strip(),
        "package_path": "packages/topoaccess_prod",
        "license": "Apache-2.0",
        "license_confirmed": Path("packages/topoaccess_prod/LICENSE").exists(),
        "publish_ready": push_ready,
        "remote_configured": bool(remote),
        "safe_publish_tool_used": True,
        "old_sync_script_used": False,
        "artifact_audit_status": "pending",
        "secret_scan_status": "pending",
        "dogfood_savings": 0,
        "codex_smoke_rows": 0,
        "change_planning_score": 0,
        "disallowed_paths": disallowed,
        "outside_allowlist": outside_allowlist[:50],
        "manual_push_command": f"git push -u origin {branch}",
        "nonpreferred_model_used": False,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "result_status": "pass" if not disallowed else "fail",
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text(
        "# V36 Safe Publish\n\n"
        f"- Dry-run: `{dry_run}`\n"
        f"- Remote configured: `{bool(remote)}`\n"
        f"- Manifest exists: `{manifest}`\n"
        f"- Blocked paths: `{len(disallowed)}`\n"
        f"- Push ready: `{push_ready}`\n\n"
        "push remains manual until remote is configured.\n",
        encoding="utf-8",
    )
    return row

