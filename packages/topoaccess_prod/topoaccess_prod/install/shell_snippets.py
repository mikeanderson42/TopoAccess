from __future__ import annotations


def snippet(target: str, profile: str = "default") -> str:
    return f"alias topoaccess-{target}='python packages/topoaccess_prod/scripts/topoaccess_agent.py workspace status --profile {profile}'"
