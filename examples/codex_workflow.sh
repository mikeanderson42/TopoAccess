#!/usr/bin/env bash
set -euo pipefail

task="${*:-What tests should I run after editing README.md?}"
topoaccess codex-brief --profile "${TOPOACCESS_PROFILE:-demo}" --task "$task"
topoaccess preflight --profile "${TOPOACCESS_PROFILE:-demo}" --task "$task"
