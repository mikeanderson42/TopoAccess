# TopoAccess v1.0.0-rc1

TopoAccess is a local, model-agnostic repo-intelligence sidecar for coding agents.

It helps Codex, Claude Code, Cursor, Aider, OpenClaw, OpenHands, Hermes/generic agents, HTTP clients, and stdio tools get compact, provenance-backed repository context before editing.

## What Changed

- Public package layout under `packages/topoaccess_prod`.
- Model-free public CI.
- Public `topoaccess_prod.cache` package restored.
- Root README and docs polished for public install and harness use.
- Release assets, checksums, and upload commands prepared.
- Exact lookup remains tool-only.
- Optional model-backed synthesis is category-gated and workspace-configured.

## Install

```bash
git clone https://github.com/mikeanderson42/TopoAccess.git
cd TopoAccess
python -m pip install -e packages/topoaccess_prod
topoaccessctl --help
```

## Use With Codex And Harnesses

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief \
  --profile default \
  --task "Plan a safe repo change"
```

HTTP, stdio, OpenAPI, and MCP-like schemas are included under `release/topoaccess_prod_v39/`.

## Safety Model

- Model-agnostic by default.
- Exact lookup never requires a model.
- Public CI is model-free.
- Local model adapters are configured by workspace profiles.
- Optional model-backed synthesis is category-gated.
- Provenance is required for audited answers.
- Unsupported requests should abstain rather than guess.

Qwen3.6-35B-A3B-uncensored-heretic-APEX-I-Compact was used for local validation only and is not a required public dependency.

## Checks Passed

- Product tests: 67 passed.
- Compileall: passed.
- Editable install: passed.
- CLI help: passed.
- Artifact audit: 0 failures.
- Secret scan: 0 failures.
- Conformance: 8 checks, 0 failures.

## Known Limitations

- Native service installation remains operator action.
- External harness behavior depends on installed tool versions.
- Private local caches/models are intentionally not included.
