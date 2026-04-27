#!/usr/bin/env bash
set -euo pipefail
python -m pytest packages/topoaccess_prod/tests
python packages/topoaccess_prod/scripts/topoaccessctl.py validate-release --cache cache/topoaccess_v21 --release release/topoaccess_prod
python packages/topoaccess_prod/scripts/topoaccess_artifact_audit.py --paths packages/topoaccess_prod release/topoaccess_prod_v37 --out runs/topoaccess_prod_ci/artifact_audit.jsonl --report REPORT_topoaccess_prod_ci.md
python packages/topoaccess_prod/scripts/topoaccess_secret_scan.py --paths packages/topoaccess_prod release/topoaccess_prod_v37 --out runs/topoaccess_prod_ci/secret_scan.jsonl --report REPORT_topoaccess_prod_ci.md
python packages/topoaccess_prod/scripts/topoaccess_adapter_smoke.py --profile default --targets codex claude-code openclaw hermes generic http stdio
python packages/topoaccess_prod/scripts/topoaccess_conformance_check.py --release release/topoaccess_prod_v37 --out runs/topoaccess_prod_ci/conformance.jsonl --report REPORT_topoaccess_prod_ci.md
