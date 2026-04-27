from __future__ import annotations

import json
from pathlib import Path

from .agents_md import base_row


def generate_claude_hooks(profile: str, out: str, report: str) -> dict:
    out_dir = Path(out); out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "settings.example.json"
    hooks = {
        "hooks": {
            "SessionStart": [{"type": "command", "command": "python packages/topoaccess_prod/scripts/topoaccess_agent.py workspace status --profile default"}],
            "PreToolUse": [{"matcher": "Edit|Write|Bash", "type": "command", "command": "echo 'TopoAccess preflight/test-impact recommended; destructive commands are not auto-run.'"}],
            "PostToolUse": [{"matcher": "Edit|Write", "type": "command", "command": "python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile default --changed-files \"$CLAUDE_FILE\""}],
        }
    }
    target.write_text(json.dumps(hooks, indent=2, sort_keys=True), encoding="utf-8")
    row = base_row("claude_hooks", str(target))
    Path("runs/topoaccess_prod_v37/claude_hooks.jsonl").write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    with Path(report).open("a", encoding="utf-8") as f:
        f.write("\nClaude hooks example generated.\n")
    return row

