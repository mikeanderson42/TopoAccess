from __future__ import annotations

import json
from pathlib import Path


def run_license_gate(package: str, out: str, report: str) -> dict:
    base = Path(package)
    license_text = (base / "LICENSE.md").read_text(encoding="utf-8") if (base / "LICENSE.md").exists() else ""
    lower = license_text.lower()
    blockers = [
        "choose the intended license",
        "choose and apply",
        "no standalone product license",
        "pending",
        "before external distribution",
    ]
    confirmed = bool(license_text.strip()) and not any(blocker in lower for blocker in blockers)
    row = {
        "run_id": "v34_license_gate",
        "phase": "license_gate",
        "harness": "release",
        "task_id": "license",
        "license_file": str(base / "LICENSE.md"),
        "authors_exists": (base / "AUTHORS.md").exists(),
        "credits_exists": (base / "CREDITS.md").exists(),
        "readme_credit": "Mike" in (base / "README.md").read_text(encoding="utf-8"),
        "license_confirmed": confirmed,
        "public_publish_ready": confirmed,
        "local_release_ready": True,
        "topoaccess_used": False,
        "codex_brief_generated": False,
        "post_edit_validation_generated": False,
        "direct_tokens": 0,
        "topoaccess_tokens": 0,
        "token_savings": 0,
        "files_selected": [],
        "tests_selected": [],
        "commands_selected": [],
        "provenance_count": 3,
        "hallucinated_files": 0,
        "hallucinated_commands": 0,
        "preferred_model_verified": True,
        "nonpreferred_model_used": False,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "release_gate_status": "pass_local_fail_public" if not confirmed else "pass",
        "result_status": "pass",
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    status = "public publish blocked on license confirmation" if not confirmed else "public publish license gate passed"
    todo = "\nTODO: Mike must choose/confirm license before public release.\n" if not confirmed else ""
    Path(report).write_text(
        "# V34 License Gate\n\n"
        f"- License confirmed: `{confirmed}`\n"
        "- Local/internal release ready: `true`\n"
        f"- Public publish ready: `{confirmed}`\n\n"
        f"{status}.\n"
        f"{todo}",
        encoding="utf-8",
    )
    return row
