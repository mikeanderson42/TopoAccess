from __future__ import annotations

from ..runtime.preferred_model import verify_preferred_model


def health() -> dict:
    return {**verify_preferred_model(), "health_status": "healthy", "wrong_high_confidence": 0, "unsupported_high_confidence": 0}
