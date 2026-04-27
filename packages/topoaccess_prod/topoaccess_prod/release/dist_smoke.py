from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def dist_smoke(package: str, out: str, report: str) -> dict:
    import_proc = subprocess.run([sys.executable, "-c", "import topoaccess_prod; print(topoaccess_prod.__version__)"], cwd=package, text=True, capture_output=True)
    cli_proc = subprocess.run([sys.executable, "scripts/topoaccessctl.py", "--help"], cwd=package, text=True, capture_output=True)
    row = {
        "run_id": "v36_dist_smoke",
        "phase": "dist_smoke",
        "command": "topoaccess_dist_smoke",
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
        "import_returncode": import_proc.returncode,
        "cli_returncode": cli_proc.returncode,
        "nonpreferred_model_used": False,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "result_status": "pass" if import_proc.returncode == 0 and cli_proc.returncode == 0 else "fail",
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text(f"# V36 Distribution Smoke\n\n- Import: `{import_proc.returncode}`\n- CLI help: `{cli_proc.returncode}`\n", encoding="utf-8")
    return row

