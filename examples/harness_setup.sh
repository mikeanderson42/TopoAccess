#!/usr/bin/env bash
set -euo pipefail

profile="${TOPOACCESS_PROFILE:-demo}"

topoaccess setup codex --profile "$profile" --dry-run
topoaccess setup claude --profile "$profile" --dry-run
topoaccess setup cursor --profile "$profile" --dry-run
topoaccess setup aider --profile "$profile" --dry-run
topoaccess setup openclaw --profile "$profile" --dry-run
topoaccess setup openhands --profile "$profile" --dry-run
topoaccess setup hermes --profile "$profile" --dry-run
topoaccess setup generic --profile "$profile" --dry-run
topoaccess setup http --profile "$profile" --dry-run
topoaccess setup stdio --profile "$profile" --dry-run
