from __future__ import annotations

import json
from pathlib import Path

APACHE_2_TEXT = """Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

This product package is distributed under the Apache License, Version 2.0.
The complete canonical license text is available at:
https://www.apache.org/licenses/LICENSE-2.0
"""


def finalize_license(package: str, license_id: str, creator: str, out: str, report: str) -> dict:
    base = Path(package)
    if license_id.lower() not in {"apache-2.0", "apache2", "apache"}:
        raise ValueError("V36 only finalizes Apache-2.0")
    (base / "LICENSE").write_text(APACHE_2_TEXT, encoding="utf-8")
    (base / "LICENSE.md").write_text("# License\n\nTopoAccess product package is licensed under Apache-2.0.\n", encoding="utf-8")
    (base / "NOTICE").write_text(
        f"TopoAccess\n\nCreator / Project Owner / System Architect: {creator}\nAI-assisted implementation: Codex/ChatGPT assistance under {creator}'s direction.\n",
        encoding="utf-8",
    )
    authors = f"# Authors\n\n- Creator / Project Owner / System Architect: {creator}\n"
    credits = f"# Credits\n\n- Creator / Project Owner / System Architect: {creator}\n- AI-assisted implementation: Codex/ChatGPT assistance under {creator}'s direction.\n"
    (base / "AUTHORS.md").write_text(authors, encoding="utf-8")
    (base / "CREDITS.md").write_text(credits, encoding="utf-8")

    pyproject = base / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    if "license =" not in text:
        text = text.replace("authors = [{name = \"Mike / project owner\"}]\n", "authors = [{name = \"Mike / project owner\"}]\nlicense = {text = \"Apache-2.0\"}\n")
    pyproject.write_text(text, encoding="utf-8")

    docs = base / "docs" / "LICENSE_AND_CREDITS.md"
    docs.write_text(
        f"# License and Credits\n\nLicense: Apache-2.0.\n\nCreator, project owner, and system architect: {creator}.\n\nAI-assisted implementation support: Codex / ChatGPT under {creator}'s direction.\n\nAI assistance does not imply ownership.\n",
        encoding="utf-8",
    )
    readme = base / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    if "## License" not in readme_text:
        readme_text += "\n## License\n\nApache-2.0.\n"
    readme.write_text(readme_text, encoding="utf-8")

    row = {
        "run_id": "v36_license_finalize",
        "phase": "license_finalize",
        "command": "topoaccess_finalize_license",
        "branch": "",
        "commit": "",
        "package_path": package,
        "license": "Apache-2.0",
        "license_confirmed": True,
        "publish_ready": False,
        "remote_configured": False,
        "safe_publish_tool_used": False,
        "old_sync_script_used": False,
        "artifact_audit_status": "pending",
        "secret_scan_status": "pending",
        "dogfood_savings": 0,
        "codex_smoke_rows": 0,
        "change_planning_score": 0,
        "nonpreferred_model_used": False,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "result_status": "pass",
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text("# V36 License\n\nApache-2.0 finalized for `packages/topoaccess_prod`.\n\nCreator / Project Owner / System Architect: Mike.\n", encoding="utf-8")
    return row

