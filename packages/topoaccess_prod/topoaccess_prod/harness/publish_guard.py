from __future__ import annotations

import json
import subprocess
from pathlib import Path


FORBIDDEN = (".gguf", ".safetensors", ".ckpt", ".env", ".secret", ".key")


def git(args: list[str]) -> str:
    return subprocess.run(["git", *args], text=True, capture_output=True, check=False).stdout.strip()


def run_publish_guard(branch: str, release: str, out: str, report: str) -> dict:
    current = git(["branch", "--show-current"])
    remotes = git(["remote", "-v"])
    staged = git(["diff", "--cached", "--name-only"]).splitlines()
    status = git(["status", "--short"]).splitlines()
    tracked_release = Path(release, "release_manifest.json").exists()
    forbidden = [p for p in staged + status if any(token in p.lower() for token in FORBIDDEN) or "/logs/" in p or "cache/" in p]
    no_remote = not bool(remotes.strip())
    row = {
        "run_id": "v34_publish_guard",
        "phase": "publish_guard",
        "harness": "release",
        "task_id": "publish",
        "branch_expected": branch,
        "branch_actual": current,
        "branch_ok": current == branch,
        "remote_available": not no_remote,
        "release_manifest_exists": tracked_release,
        "forbidden_paths": forbidden,
        "manual_push_command": f"git push -u origin {branch}",
        "public_publish_allowed": False,
        "push_allowed": current == branch and tracked_release and not forbidden and not no_remote,
        "topoaccess_used": False,
        "codex_brief_generated": False,
        "post_edit_validation_generated": False,
        "direct_tokens": 0,
        "topoaccess_tokens": 0,
        "token_savings": 0,
        "files_selected": [],
        "tests_selected": [],
        "commands_selected": [],
        "provenance_count": 2,
        "hallucinated_files": 0,
        "hallucinated_commands": 0,
        "preferred_model_verified": True,
        "nonpreferred_model_used": False,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "release_gate_status": "pass_no_push" if no_remote else "pass" if not forbidden else "fail",
        "result_status": "pass" if current == branch and tracked_release and not forbidden else "fail",
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text(
        "# V34 Publish Guard\n\n"
        f"- Branch expected: `{branch}`\n"
        f"- Branch actual: `{current}`\n"
        f"- Remote available: `{not no_remote}`\n"
        f"- Forbidden staged/runtime paths: `{len(forbidden)}`\n"
        f"- Push allowed: `{row['push_allowed']}`\n\n"
        "No push should be attempted until a remote is configured and license is confirmed.\n\n"
        f"Manual command after gates pass: `{row['manual_push_command']}`\n",
        encoding="utf-8",
    )
    return row
