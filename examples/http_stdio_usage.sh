#!/usr/bin/env bash
set -euo pipefail

# Non-blocking HTTP readiness smoke:
topoaccess serve-http --profile "${TOPOACCESS_PROFILE:-demo}" --port "${TOPOACCESS_HTTP_PORT:-8876}" --smoke

# stdio is a long-running bridge; run interactively when a harness connects:
topoaccess stdio --profile "${TOPOACCESS_PROFILE:-demo}" --help
