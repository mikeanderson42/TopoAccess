from __future__ import annotations

from pathlib import Path


def write_doc(path: str, title: str, body: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8")
