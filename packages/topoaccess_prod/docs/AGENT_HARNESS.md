# Agent Harness

TopoAccess V31 exposes the product package as a repo-intelligence sidecar for coding agents.

Use:

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py preflight --profile default --task "Add a token accounting report"
python packages/topoaccess_prod/scripts/topoaccess_agent.py test-impact --profile default --changed-file topoaccess/v29_common.py
python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile default --changed-files <files>
```

Exact lookup remains tool-only. Preferred model remains category-gated.
