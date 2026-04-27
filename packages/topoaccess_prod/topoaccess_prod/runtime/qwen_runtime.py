from __future__ import annotations

from .preferred_model import verify_preferred_model


def runtime_status() -> dict:
    return {**verify_preferred_model(), "backend": "lmstudio_openai_compat_or_wrapper", "category_gated": True}
