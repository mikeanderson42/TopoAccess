from __future__ import annotations

import json
from pathlib import Path

from .agents_md import base_row


def generate_cursor_rules(profile: str, out: str, report: str) -> dict:
    out_dir = Path(out); out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "topoaccess.mdc"
    target.write_text(
        "---\nglobs: packages/topoaccess_prod/**\n---\n"
        "Use TopoAccess preflight before edits and post-edit validation after edits. "
        "Exact lookup is tool-only. Do not commit local caches, models, GGUF files, secrets, logs, or env files. Apache-2.0 metadata applies.\n",
        encoding="utf-8",
    )
    row = base_row("cursor_rules", str(target))
    Path("runs/topoaccess_prod_v37/cursor_rules.jsonl").write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    with Path(report).open("a", encoding="utf-8") as f:
        f.write("\nCursor rules generated.\n")
    return row

