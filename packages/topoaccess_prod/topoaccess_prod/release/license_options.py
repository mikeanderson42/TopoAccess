from __future__ import annotations

import json
from pathlib import Path


OPTIONS = [
    {"id": "mit", "name": "MIT", "pros": ["simple", "permissive", "common for local tools"], "cons": ["minimal patent language"]},
    {"id": "apache-2.0", "name": "Apache-2.0", "pros": ["permissive", "explicit patent grant"], "cons": ["longer notice requirements"]},
    {"id": "busl-private", "name": "BUSL/private", "pros": ["commercial control"], "cons": ["less frictionless for community use"]},
    {"id": "internal-private", "name": "Internal/private placeholder", "pros": ["safe before public release"], "cons": ["blocks public distribution"]},
]


def license_confirmed(package: str) -> bool:
    text = (Path(package) / "LICENSE.md").read_text(encoding="utf-8") if (Path(package) / "LICENSE.md").exists() else ""
    lower = text.lower()
    blockers = ["no standalone product license", "choose and apply", "choose the intended license", "before external distribution", "pending"]
    return bool(text.strip()) and not any(blocker in lower for blocker in blockers)


def write_license_options(package: str, out: str, report: str) -> list[dict]:
    confirmed = license_confirmed(package)
    rows = []
    for option in OPTIONS:
        rows.append({
            "run_id": f"v35_license_{option['id']}",
            "phase": "license_options",
            "command": "topoaccess_license_options",
            "package_path": package,
            "branch": "",
            "commit": "",
            "sync_script_found": False,
            "sync_script_used": False,
            "sync_script_mode": "none",
            "license_confirmed": confirmed,
            "public_publish_ready": confirmed,
            "local_release_ready": True,
            "harness": "release",
            "task_category": "license",
            "token_savings": 0,
            "files_selected": [str(Path(package) / "LICENSE.md")],
            "tests_selected": [],
            "commands_selected": [],
            "provenance_count": 2,
            "nonpreferred_model_used": False,
            "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
            "license_option": option,
            "result_status": "pass",
        })
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    lines = ["# V35 License Options", "", f"- License confirmed: `{confirmed}`", "- Public publish ready: `" + str(confirmed).lower() + "`", "", "## Options"]
    lines += [f"- `{o['id']}`: {o['name']} | pros: {', '.join(o['pros'])} | cons: {', '.join(o['cons'])}" for o in OPTIONS]
    if not confirmed:
        lines += ["", "public publish remains blocked on license confirmation."]
    Path(report).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return rows

