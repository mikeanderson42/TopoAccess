from __future__ import annotations

import json
import tarfile
from pathlib import Path

from .distribution_builder import SAFE_DIRS, SAFE_FILES, _base_row


def build_release_archive(package: str, release: str, out: str, report: str) -> dict:
    pkg = Path(package)
    release_dir = Path(release)
    archive_dir = release_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive = archive_dir / "topoaccess-prod-v38-release.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for child in pkg.iterdir():
            if child.name in SAFE_DIRS or child.name in SAFE_FILES:
                tar.add(child, arcname=f"topoaccess_prod/{child.name}")
        for child in release_dir.iterdir():
            if child.name != "archive":
                tar.add(child, arcname=f"release/topoaccess_prod_v38/{child.name}")
    row = _base_row("release_archive", "topoaccess_release_archive", str(archive))
    row.update({"archive_exists": archive.exists(), "archive_bytes": archive.stat().st_size})
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    with Path(report).open("a", encoding="utf-8") as f:
        f.write(f"\n## Release Archive\n\n- Archive: `{archive}`\n- Bytes: `{row['archive_bytes']}`\n")
    return row

