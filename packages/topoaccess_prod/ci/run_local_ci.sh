#!/usr/bin/env bash
set -euo pipefail
python -m pytest packages/topoaccess_prod/tests
python -m compileall packages/topoaccess_prod
topoaccessctl --help
python packages/topoaccess_prod/scripts/topoaccess_artifact_audit.py --paths packages/topoaccess_prod .github README.md docs examples LICENSE NOTICE CHANGELOG.md CONTRIBUTING.md SECURITY.md release_notes.md --out runs/topoaccess_prod_ci/artifact_audit.jsonl --report REPORT_topoaccess_prod_ci.md
python packages/topoaccess_prod/scripts/topoaccess_secret_scan.py --paths packages/topoaccess_prod .github README.md docs examples LICENSE NOTICE CHANGELOG.md CONTRIBUTING.md SECURITY.md release_notes.md --out runs/topoaccess_prod_ci/secret_scan.jsonl --report REPORT_topoaccess_prod_ci.md
python packages/topoaccess_prod/scripts/topoaccess_adapter_smoke.py --profile default --targets codex claude-code openclaw hermes generic http stdio
python packages/topoaccess_prod/scripts/topoaccess_conformance_check.py --release examples/integrations --out runs/topoaccess_prod_ci/conformance.jsonl --report REPORT_topoaccess_prod_ci.md
