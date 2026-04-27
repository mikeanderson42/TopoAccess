# AGENTS.md

TopoAccess is a local repo-intelligence sidecar for coding agents.

Rules:
- Use TopoAccess for exact lookup; exact lookup is tool-only.
- TopoAccess is model-agnostic by default; optional model-backed synthesis is category-gated only for change planning, model-required narrative, report synthesis, and troubleshooting.
- Exact lookup never requires a model.
- Run preflight before edits: `python packages/topoaccess_prod/scripts/topoaccess_agent.py preflight --profile default --task "<task>"`.
- Run post-edit validation after edits: `python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile default --changed-files <files>`.
- Run product tests: `python -m pytest packages/topoaccess_prod/tests`.
- Run release validation: `python packages/topoaccess_prod/scripts/topoaccessctl.py validate-release --cache cache/topoaccess_v21 --release release/topoaccess_prod`.
- Do not commit model files, GGUFs, cache blobs, logs, secrets, or env files.
- Provenance is required for audited answers.
- Use safe publish dry-run before branch publication.
