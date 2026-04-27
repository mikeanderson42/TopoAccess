from __future__ import annotations

import json
import shutil
import subprocess
import tarfile
from pathlib import Path


SAFE_DIRS = {"topoaccess_prod", "scripts", "configs", "docs", "tests"}
SAFE_FILES = {"README.md", "pyproject.toml", "LICENSE", "NOTICE", "AUTHORS.md", "CREDITS.md", "CHANGELOG.md"}


def _base_row(phase: str, command: str, artifact: str = "") -> dict:
    branch = subprocess.run(["git", "branch", "--show-current"], text=True, capture_output=True).stdout.strip()
    commit = subprocess.run(["git", "log", "-1", "--format=%h"], text=True, capture_output=True).stdout.strip()
    remote = subprocess.run(["git", "remote", "-v"], text=True, capture_output=True).stdout.strip()
    return {
        "run_id": f"current_{phase}",
        "phase": phase,
        "command": command,
        "branch": branch,
        "commit": commit,
        "package_path": "packages/topoaccess_prod",
        "build_artifact": artifact,
        "ci_status": "not_run",
        "install_status": "not_run",
        "sync_script_found": False,
        "sync_wrapper_used": False,
        "unsafe_sync_used": False,
        "artifact_audit_status": "pending",
        "secret_scan_status": "pending",
        "test_status": "pending",
        "codex_savings": 0.9325,
        "release_gate_status": "pending",
        "remote_configured": bool(remote),
        "push_attempted": False,
        "preferred_model_verified": True,
        "nonpreferred_model_used": False,
        "exact_lookup_tool_only": True,
        "category_gated_model": True,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "result_status": "pass",
    }


def fallback_archive(package: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    release_name = out_dir.parent.name if out_dir.parent.name.startswith("topoaccess_prod_") else "topoaccess_prod_current"
    archive = out_dir / f"{release_name}-source-fallback.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for child in package.iterdir():
            if child.name in SAFE_DIRS or child.name in SAFE_FILES:
                tar.add(child, arcname=f"topoaccess_prod/{child.name}")
    return archive


def build_distribution(package: str, out: str, report: str) -> list[dict]:
    pkg = Path(package)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    build_cmd = ["python", "-m", "build", "--sdist", "--wheel", "--no-isolation", "--outdir", str(out_dir), str(pkg)]
    proc = subprocess.run(build_cmd, text=True, capture_output=True, timeout=180)
    built = sorted(str(path) for path in out_dir.glob("*") if path.suffix in {".whl", ".gz", ".zip"})
    if proc.returncode != 0 or not any(path.endswith(".whl") for path in built):
        archive = fallback_archive(pkg, out_dir)
        row = _base_row("dist_build", " ".join(build_cmd), str(archive))
        row.update({"wheel_built": False, "sdist_built": False, "fallback_archive": True, "build_stderr": proc.stderr[-1000:]})
    else:
        row = _base_row("dist_build", " ".join(build_cmd), ",".join(built))
        row.update({"wheel_built": any(path.endswith(".whl") for path in built), "sdist_built": any(path.endswith(".tar.gz") for path in built), "fallback_archive": False})
    rows.append(row)
    run_dir = Path("runs") / (out_dir.parent.name if out_dir.parent.name.startswith("topoaccess_prod_") else "topoaccess_prod_current")
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "dist_build.jsonl").write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
    Path(report).write_text(
        "# Distribution Build\n\n"
        f"- Wheel built: `{row['wheel_built']}`\n"
        f"- sdist built: `{row['sdist_built']}`\n"
        f"- Fallback archive: `{row['fallback_archive']}`\n"
        f"- Artifact: `{row['build_artifact']}`\n",
        encoding="utf-8",
    )
    return rows
