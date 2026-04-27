from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .distribution_builder import _base_row


def run_fresh_install_smoke(package: str, dist: str, out: str, report: str) -> list[dict]:
    rows = []
    import_proc = subprocess.run(
        ["python", "-c", "import sys; sys.path.insert(0,'packages/topoaccess_prod'); import topoaccess_prod; print(topoaccess_prod.__name__)"],
        text=True,
        capture_output=True,
        timeout=30,
    )
    row = _base_row("fresh_install", "source import", "")
    row.update({"install_status": "pass" if import_proc.returncode == 0 else "fail", "source_import": import_proc.returncode == 0})
    rows.append(row)
    help_proc = subprocess.run(["python", str(Path(package) / "scripts" / "topoaccessctl.py"), "--help"], text=True, capture_output=True, timeout=30)
    row2 = _base_row("fresh_install", "topoaccessctl --help", "")
    row2.update({"install_status": "pass" if help_proc.returncode == 0 else "fail", "cli_help": help_proc.returncode == 0})
    rows.append(row2)
    wheel = next(Path(dist).glob("*.whl"), None) if Path(dist).exists() else None
    row3 = _base_row("fresh_install", "wheel presence", str(wheel) if wheel else "")
    row3.update({"install_status": "pass" if wheel else "fallback", "wheel_available": bool(wheel), "external_services_required": False})
    rows.append(row3)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
    passed = all(r["install_status"] in {"pass", "fallback"} for r in rows)
    with Path(report).open("a", encoding="utf-8") as f:
        f.write(f"\n## Fresh Install Smoke\n\n- Rows: {len(rows)}\n- Passed: `{passed}`\n- Wheel available: `{bool(wheel)}`\n")
    return rows

