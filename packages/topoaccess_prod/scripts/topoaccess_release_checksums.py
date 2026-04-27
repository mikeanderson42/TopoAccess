#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SHA256 checksums for release assets.")
    parser.add_argument("--paths", nargs="+", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", default="")
    args = parser.parse_args()

    files: list[Path] = []
    for item in args.paths:
        path = Path(item)
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file() and p.name != Path(args.out).name)

    lines = [f"{sha256(path)}  {path}" for path in sorted(files)]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    if args.report:
        Path(args.report).write_text(
            f"# V40 Release Checksums\n\n- Files checksummed: `{len(lines)}`\n- Output: `{out}`\n",
            encoding="utf-8",
        )
    print({"checksums": len(lines), "out": str(out)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
