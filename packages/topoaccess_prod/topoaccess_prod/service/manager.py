from __future__ import annotations

from topoaccess.v29_common import control


def service_status(cache: str = "cache/topoaccess_v21") -> dict:
    return control("status", cache)
