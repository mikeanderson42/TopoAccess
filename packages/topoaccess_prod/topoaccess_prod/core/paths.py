from __future__ import annotations

from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PACKAGE_ROOT.parents[1]
RUN_DIR = REPO_ROOT / "runs" / "topoaccess_prod"
RELEASE_DIR = REPO_ROOT / "release" / "topoaccess_prod"


def ensure_product_dirs() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
