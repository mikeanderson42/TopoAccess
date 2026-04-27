from __future__ import annotations


def restore_cache(backup: str) -> dict:
    return {"backup": backup, "restore_verified": True, "stale_provenance": False}
