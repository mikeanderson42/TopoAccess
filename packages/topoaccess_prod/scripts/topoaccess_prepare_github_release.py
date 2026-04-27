#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare model-free GitHub release asset metadata.")
    parser.add_argument("--release", default="release/topoaccess_prod_v39")
    parser.add_argument("--out", default="release/topoaccess_prod_v39_1/release_assets.json")
    args = parser.parse_args()

    release = Path(args.release)
    assets = [path for path in release.rglob("*") if path.is_file() and path.stat().st_size < 5_000_000]
    payload = {
        "tag": "v1.0.0-rc1",
        "title": "TopoAccess v1.0.0-rc1",
        "assets": [
            {"path": str(path), "sha256": checksum(path), "size": path.stat().st_size}
            for path in assets
        ],
        "upload_command": "gh release upload v1.0.0-rc1 <asset paths> --repo mikeanderson42/TopoAccess",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
