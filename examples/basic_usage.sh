#!/usr/bin/env bash
set -euo pipefail

python -m pip install -e packages/topoaccess_prod
topoaccess --help
topoaccess init
topoaccess try
topoaccess codex-brief --profile demo --task "What tests should I run after editing README.md?"
