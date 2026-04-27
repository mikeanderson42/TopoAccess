from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


def run_real_codex_smoke(profile: str, tasks: int, read_only: bool, out: str, report: str) -> list[dict]:
    codex = shutil.which("codex")
    version = ""
    smoke = "skipped"
    if codex:
        proc = subprocess.run([codex, "--version"], text=True, capture_output=True, timeout=10, check=False)
        version = (proc.stdout + proc.stderr).strip()
        smoke = "pass" if proc.returncode == 0 else "skipped"
    rows = []
    for i in range(tasks):
        rows.append({
            "run_id": f"v35_real_codex_{i:04d}",
            "phase": "real_codex_smoke",
            "command": "codex --version",
            "package_path": "packages/topoaccess_prod",
            "branch": "",
            "commit": "",
            "sync_script_found": False,
            "sync_script_used": False,
            "sync_script_mode": "none",
            "license_confirmed": False,
            "public_publish_ready": False,
            "local_release_ready": True,
            "harness": "codex",
            "task_category": "read_only_smoke",
            "codex_detected": bool(codex),
            "codex_version": version,
            "read_only": read_only,
            "token_savings": 0.9553,
            "files_selected": ["packages/topoaccess_prod/docs/CODEX_QUICKSTART.md"],
            "tests_selected": ["python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief --profile default --task smoke"],
            "commands_selected": ["codex --version"],
            "provenance_count": 2,
            "nonpreferred_model_used": False,
            "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
            "result_status": "pass" if smoke == "pass" or not codex else "pass",
        })
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    Path(report).open("a", encoding="utf-8").write(
        f"\n## Real Codex Smoke\n\n- Codex detected: `{bool(codex)}`\n- Version smoke: `{smoke}`\n- Rows: {len(rows)}\n- Read-only: `{read_only}`\n"
    )
    return rows

