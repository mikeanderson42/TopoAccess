from __future__ import annotations

from topoaccess.provenance import stable_hash


def new_trace_id(seed: str) -> str:
    return stable_hash(["topoaccess_prod", seed])
