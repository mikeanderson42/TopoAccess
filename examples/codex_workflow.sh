#!/usr/bin/env bash
set -euo pipefail

task="${*:-What tests should I run after editing README.md?}"
topoaccess init
topoaccess codex-brief --profile "${TOPOACCESS_PROFILE:-demo}" --task "$task"
topoaccess preflight --profile "${TOPOACCESS_PROFILE:-demo}" --task "$task"
topoaccess post-edit --profile "${TOPOACCESS_PROFILE:-demo}" --changed-files README.md
