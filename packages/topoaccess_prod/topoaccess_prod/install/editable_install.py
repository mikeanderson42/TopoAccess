from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def editable_install_smoke(package: str, dry_run_first: bool, out: str, report: str) -> dict:
    check = subprocess.run([sys.executable, "-m", "pip", "install", "-e", package, "--dry-run"], text=True, capture_output=True)
    installed = False
    install_code = None
    if check.returncode == 0 and not dry_run_first:
        proc = subprocess.run([sys.executable, "-m", "pip", "install", "-e", package], text=True, capture_output=True)
        install_code = proc.returncode
        installed = proc.returncode == 0
    row = {
        "run_id": "v36_editable_install",
        "phase": "editable_install",
        "command": "topoaccess_editable_install_smoke",
        "branch": "",
        "commit": "",
        "package_path": package,
        "license": "Apache-2.0",
        "license_confirmed": Path(package, "LICENSE").exists(),
        "publish_ready": False,
        "remote_configured": False,
        "safe_publish_tool_used": False,
        "old_sync_script_used": False,
        "artifact_audit_status": "pending",
        "secret_scan_status": "pending",
        "dogfood_savings": 0,
        "codex_smoke_rows": 0,
        "change_planning_score": 0,
        "dry_run_returncode": check.returncode,
        "installed": installed,
        "install_returncode": install_code,
        "nonpreferred_model_used": False,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "result_status": "pass" if check.returncode == 0 else "fail",
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    with Path(report).open("a", encoding="utf-8") as f:
        f.write(f"\n## Editable Install\n\n- Dry-run return code: `{check.returncode}`\n- Installed: `{installed}`\n")
    return row

