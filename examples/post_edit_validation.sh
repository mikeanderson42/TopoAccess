#!/usr/bin/env bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile default --changed-files "$@"
