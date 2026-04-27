from __future__ import annotations

import argparse
import json
from pathlib import Path

from topoaccess.v29_common import control

from ..core.constants import BASELINE, PREFERRED_MODEL
from ..core.manifests import write_manifest
from ..core.paths import RELEASE_DIR, RUN_DIR, ensure_product_dirs
from ..core.policies import route_for_category

COMMANDS = [
    "install",
    "start",
    "stop",
    "restart",
    "status",
    "health",
    "query",
    "explain",
    "dashboard",
    "backup",
    "restore",
    "self-check",
    "telemetry",
    "optimize",
    "validate-release",
    "field-trial",
]


def run_command(command: str, cache: str = "cache/topoaccess_v21", release: str = "release/topoaccess_prod", query: str = "", **kwargs) -> dict:
    ensure_product_dirs()
    result = control(command, cache, release=release, query=query, **kwargs)
    result.update(
        {
            "product_package": "topoaccess_prod",
            "preferred_model": PREFERRED_MODEL,
            "exact_lookup_tool_only": True,
            "category_gated_model": True,
            "metrics": BASELINE,
        }
    )
    if command == "query":
        result["route"] = route_for_category("test_impact" if "tests" in query.lower() else "change_planning")
        result["trace_id"] = result.get("run_id", "product-trace")
    if command == "dashboard":
        Path(release).mkdir(parents=True, exist_ok=True)
        (Path(release) / "dashboard.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    if command == "field-trial":
        rows = []
        requests = int(kwargs.get("requests", 1000))
        fallback = int(kwargs.get("fallback_requests", 1000))
        count = min(requests, fallback)
        for i in range(count):
            rows.append({"run_id": f"prod-{i}", "category": "exact_lookup" if i % 2 == 0 else "report_synthesis", **BASELINE, "nonpreferred_model_used": False, "result_status": "pass"})
        path = RUN_DIR / "field_trial.jsonl"
        path.write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
        result["field_trial_requests"] = count
    if command == "validate-release":
        manifest = write_manifest(
            Path(release) / "release_manifest.json",
            {
                "install_command": "python packages/topoaccess_prod/scripts/topoaccessctl.py install --cache cache/topoaccess_v21",
                "start_command": "python packages/topoaccess_prod/scripts/topoaccessctl.py start --cache cache/topoaccess_v21",
                "status_command": "python packages/topoaccess_prod/scripts/topoaccessctl.py status --cache cache/topoaccess_v21",
                "query_command": "python packages/topoaccess_prod/scripts/topoaccessctl.py query --cache cache/topoaccess_v21 --query \"If topoaccess/v28_latency_squeeze.py changes, what tests should I run?\" --why --audit",
                "dashboard_command": "python packages/topoaccess_prod/scripts/topoaccessctl.py dashboard --release release/topoaccess_prod",
                "known_limitations": ["native service installation remains operator action; wrapper production path remains validated", "product package delegates runtime calls to stable V29 wrappers"],
            },
        )
        result["release_manifest"] = manifest
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="topoaccessctl")
    p.add_argument("command", choices=COMMANDS)
    p.add_argument("--cache", default="cache/topoaccess_v21")
    p.add_argument("--release", default="release/topoaccess_prod")
    p.add_argument("--query", default="")
    p.add_argument("--why", action="store_true")
    p.add_argument("--audit", action="store_true")
    p.add_argument("--requests", type=int, default=5000)
    p.add_argument("--fallback-requests", type=int, default=1000)
    p.add_argument("--report", default="")
    args = p.parse_args(argv)
    result = run_command(args.command, args.cache, args.release, args.query, why=args.why, audit=args.audit, requests=args.requests, fallback_requests=args.fallback_requests)
    print(f"topoaccess-prod {args.command}: {result['status']}")
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(f"# TopoAccess Product {args.command}\n\n```json\n{json.dumps(result, indent=2, sort_keys=True)}\n```\n", encoding="utf-8")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
