from __future__ import annotations

from dataclasses import dataclass

from .constants import PREFERRED_MODEL


@dataclass(frozen=True)
class ProductConfig:
    cache: str = "cache/topoaccess_v21"
    release: str = "release/topoaccess_prod"
    preferred_model: str = PREFERRED_MODEL
    service_backend: str = "wrapper"


def default_config() -> ProductConfig:
    return ProductConfig()
