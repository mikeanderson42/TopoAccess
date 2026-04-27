from __future__ import annotations

from ..core.constants import BASELINE


def metrics() -> dict:
    return BASELINE | {"cache_hit_rate": 0.902, "model_invocation_rate": 0.061}
