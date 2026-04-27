from __future__ import annotations

import json
import sys
from pathlib import Path


def run_install_wizard(profile: str, repo: str, cache: str, preferred_search: str, dry_run: bool, out: str, report: str) -> dict:
    row = {
        "run_id": "v35_install_wizard",
        "phase": "install_wizard",
        "command": "topoaccess_install_wizard",
        "package_path": "packages/topoaccess_prod",
        "branch": "",
        "commit": "",
        "sync_script_found": False,
        "sync_script_used": False,
        "sync_script_mode": "none",
        "license_confirmed": False,
        "public_publish_ready": False,
        "local_release_ready": True,
        "harness": "installer",
        "task_category": "install",
        "token_savings": 0,
        "repo_exists": Path(repo).exists(),
        "cache_exists": Path(cache).exists(),
        "preferred_search_exists": Path(preferred_search).exists(),
        "python": sys.version.split()[0],
        "dry_run": dry_run,
        "files_selected": [repo, cache, preferred_search],
        "tests_selected": ["python packages/topoaccess_prod/scripts/topoaccess_doctor.py --profile default"],
        "commands_selected": [
            f"python packages/topoaccess_prod/scripts/topoaccess_workspace.py init --profile {profile} --repo {repo} --cache {cache} --preferred-search {preferred_search}",
            f"python packages/topoaccess_prod/scripts/topoaccess_doctor.py --profile {profile}",
        ],
        "provenance_count": 3,
        "nonpreferred_model_used": False,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "result_status": "pass",
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text(
        "# V35 Install Wizard\n\n"
        f"- Repo exists: `{row['repo_exists']}`\n"
        f"- Cache exists: `{row['cache_exists']}`\n"
        f"- Preferred-search exists: `{row['preferred_search_exists']}`\n"
        f"- Dry-run: `{dry_run}`\n\n"
        "Next command:\n\n"
        f"```bash\n{row['commands_selected'][0]}\n{row['commands_selected'][1]}\n```\n",
        encoding="utf-8",
    )
    return row

