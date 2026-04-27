from __future__ import annotations


POLICY = {
    "read_first": True,
    "plan_only_unless_apply": True,
    "no_hidden_writes": True,
    "exact_lookup_model_bypass": True,
    "provenance_required": True,
    "unsupported_abstention": True,
    "nonpreferred_model_fail": True,
    "no_secret_exfiltration": True,
    "no_external_network_required": True,
    "dry_run_installers_by_default": True,
}


def validate_policy() -> dict:
    return {"phase": "security_policy", "result_status": "pass" if all(POLICY.values()) else "fail", "policy": POLICY}

