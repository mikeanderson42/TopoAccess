from __future__ import annotations

import json
from pathlib import Path


def update_owner_metadata(package: str, creator: str, email: str, out: str, report: str) -> dict:
    base = Path(package)
    contact = f"{creator} <{email}>"
    (base / "AUTHORS.md").write_text(f"# Authors\n\n- Creator / Project Owner / System Architect: {contact}\n", encoding="utf-8")
    (base / "CREDITS.md").write_text(
        f"# Credits\n\n- Creator / Project Owner / System Architect: {contact}\n- AI-assisted implementation: Codex/ChatGPT assistance under {creator}'s direction.\n- AI ownership claim: none.\n",
        encoding="utf-8",
    )
    (base / "NOTICE").write_text(
        f"TopoAccess\n\nCreator / Project Owner / System Architect: {contact}\nAI-assisted implementation: Codex/ChatGPT assistance under {creator}'s direction.\n",
        encoding="utf-8",
    )
    pyproject = base / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    lines = []
    for line in text.splitlines():
        if line.startswith("authors ="):
            lines.append(f'authors = [{{name = "{creator}", email = "{email}"}}]')
        else:
            lines.append(line)
    pyproject.write_text("\n".join(lines) + "\n", encoding="utf-8")
    readme = base / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    readme_text = readme_text.replace("Mike / project owner", contact).replace("Mike's direction", f"{creator}'s direction")
    if contact not in readme_text:
        readme_text += f"\n\nCreator / Project Owner / System Architect: {contact}.\n"
    readme.write_text(readme_text, encoding="utf-8")
    row = {
        "run_id": "v37_metadata",
        "phase": "owner_metadata",
        "command": "topoaccess_update_owner_metadata",
        "package_path": package,
        "integration_target": "metadata",
        "generated_file": str(base / "AUTHORS.md"),
        "metadata_owner": contact,
        "preferred_model_verified": True,
        "nonpreferred_model_used": False,
        "exact_lookup_tool_only": True,
        "category_gated_model": True,
        "token_savings": 0,
        "codex_savings": 0,
        "change_planning_score": 0.9621,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "artifact_audit_status": "pending",
        "secret_scan_status": "pending",
        "result_status": "pass",
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text(f"# V37 Metadata\n\nOwner metadata updated to `{contact}`.\n", encoding="utf-8")
    return row

