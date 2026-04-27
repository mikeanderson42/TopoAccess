from __future__ import annotations

from pathlib import Path


def validate_install_snippets(release_dir: str = "release/topoaccess_prod_v33") -> dict:
    installers = Path(release_dir) / "installers"
    required = ["codex.md", "claude_code.md", "openclaw.md", "hermes_generic.md", "http_tool_server.md", "stdio_tool.md", "tool_schema.json"]
    missing = [name for name in required if not (installers / name).exists()]
    return {
        "phase": "install_validator",
        "release_dir": release_dir,
        "missing": missing,
        "installer_count": len(required) - len(missing),
        "result_status": "pass" if not missing else "fail",
    }
