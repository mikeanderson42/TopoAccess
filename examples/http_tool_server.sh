#!/usr/bin/env bash
python packages/topoaccess_prod/scripts/topoaccess_http_tool_server.py --profile "${TOPOACCESS_PROFILE:-demo}" --port "${TOPOACCESS_HTTP_PORT:-8876}"
