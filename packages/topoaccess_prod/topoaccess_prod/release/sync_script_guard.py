from __future__ import annotations

import json
import subprocess
from pathlib import Path


DANGEROUS = ["git add -A", "git push", "rm -rf", "git reset --hard", "remote set-url"]


def inspect_sync_script(candidates: list[str], branch: str, dry_run_only: bool, out: str, report: str) -> dict:
    found = next((Path(c).expanduser() for c in candidates if Path(c).expanduser().exists()), None)
    content = found.read_text(encoding="utf-8", errors="replace").splitlines()[:200] if found else []
    dangerous = [pattern for pattern in DANGEROUS if any(pattern in line for line in content)]
    supports_help = any("--help" in line or "-h" in line for line in content)
    supports_dry_run = any("--dry-run" in line for line in content)
    help_output = ""
    if found and supports_help:
        proc = subprocess.run([str(found), "--help"], text=True, capture_output=True, timeout=10, check=False)
        help_output = (proc.stdout + proc.stderr)[-2000:]
    safe_dry_run = bool(found and supports_dry_run and not dangerous)
    row = {
        "run_id": "v35_sync_guard",
        "phase": "sync_guard",
        "command": "topoaccess_sync_guard",
        "package_path": "packages/topoaccess_prod",
        "branch": branch,
        "commit": "",
        "sync_script_found": bool(found),
        "sync_script_path": str(found) if found else "",
        "sync_script_used": False,
        "sync_script_mode": "help_only" if help_output else "inspect_only",
        "sync_script_safe_dry_run": safe_dry_run,
        "dangerous_patterns": dangerous,
        "supports_help": supports_help,
        "supports_dry_run": supports_dry_run,
        "help_output_excerpt": help_output,
        "license_confirmed": False,
        "public_publish_ready": False,
        "local_release_ready": True,
        "harness": "release",
        "task_category": "sync",
        "token_savings": 0,
        "files_selected": [str(found)] if found else [],
        "tests_selected": [],
        "commands_selected": [f"{found} --help"] if found and supports_help else [],
        "provenance_count": 1 if found else 0,
        "nonpreferred_model_used": False,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "result_status": "pass",
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text(
        "# V35 Sync Script Guard\n\n"
        f"- Found: `{bool(found)}`\n"
        f"- Path: `{str(found) if found else ''}`\n"
        f"- Supports dry-run: `{supports_dry_run}`\n"
        f"- Dangerous patterns: `{', '.join(dangerous) if dangerous else 'none'}`\n"
        f"- Safe automatic sync: `{safe_dry_run}`\n\n"
        "If sync script is unsafe or unclear, do not use it.\n",
        encoding="utf-8",
    )
    return row

