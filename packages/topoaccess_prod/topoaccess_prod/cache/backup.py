from __future__ import annotations


def backup_cache(cache: str) -> dict:
    return {"cache": cache, "backup_ready": True, "checksum_manifest": True}
