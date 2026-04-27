from __future__ import annotations

from ..core.constants import PREFERRED_MODEL


def verify_preferred_model(model: str = PREFERRED_MODEL) -> dict:
    return {"preferred_model": PREFERRED_MODEL, "preferred_model_verified": model == PREFERRED_MODEL, "nonpreferred_model_used": model != PREFERRED_MODEL}
