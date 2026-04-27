#!/usr/bin/env bash
set -euo pipefail

python -m pip install -e packages/topoaccess_prod
topoaccess --help
topoaccess workspace init --profile demo --repo . --cache .topoaccess/cache
topoaccess doctor --profile demo
topoaccess codex-brief --profile demo --task "What tests should I run after editing README.md?"
