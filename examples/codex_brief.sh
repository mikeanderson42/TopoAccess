#!/usr/bin/env bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief --profile "${TOPOACCESS_PROFILE:-demo}" --task "$*"
