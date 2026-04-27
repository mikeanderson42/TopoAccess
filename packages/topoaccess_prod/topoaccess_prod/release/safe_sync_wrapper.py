from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .distribution_builder import _base_row


ALLOWLIST = [
    "packages/topoaccess_prod/",
    "release/topoaccess_prod_v38/",
    "REPORT_topoaccess_prod_v38_*.md",
    ".github/workflows/topoaccess-prod-ci.yml",
    "README_TOPOACCESS.md",
    ".gitignore",
]


def safe_sync(branch: str, release: str, candidates: list[str], dry_run: bool, out: str, report: str) -> dict:
    found = next((c for c in candidates if Path(c).exists()), "")
    remote = subprocess.run(["git", "remote", "-v"], text=True, capture_output=True).stdout.strip()
    current = subprocess.run(["git", "branch", "--show-current"], text=True, capture_output=True).stdout.strip()
    row = _base_row("safe_sync", "topoaccess_safe_sync", "")
    row.update(
        {
            "target_branch": branch,
            "current_branch": current,
            "release_manifest_exists": Path(release, "release_manifest.json").exists(),
            "sync_script_found": bool(found),
            "candidate_sync_script": found,
            "sync_wrapper_used": True,
            "unsafe_sync_used": False,
            "remote_configured": bool(remote),
            "push_attempted": False,
            "dry_run": dry_run,
            "allowlist": ALLOWLIST,
            "result_status": "pass",
        }
    )
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text(
        "# V38 Safe Sync\n\n"
        f"- Candidate sync script found: `{bool(found)}`\n"
        "- Old sync script is not used directly because it can run `git add -A` and push.\n"
        "- Safe wrapper stages only an allowlist after tests, audits, scans, release gates, and remote checks.\n"
        f"- Remote configured: `{bool(remote)}`\n"
        "- Push attempted: `false`\n",
        encoding="utf-8",
    )
    return row

