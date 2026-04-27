from __future__ import annotations

from topoaccess.v29_common import topograph_hash


def current_topograph_hash() -> str:
    return topograph_hash()
