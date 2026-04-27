# TopoAccess v1.0.0-rc1

TopoAccess is a local, model-agnostic repo-intelligence sidecar for coding agents.

## Highlights

- Clean public release-candidate surface.
- Current benchmark summary in `docs/BENCHMARKS.md`.
- Model-free public CI.
- Exact lookup remains tool-only.
- Optional model-backed synthesis is category-gated and workspace-configured.
- Apache-2.0 license and Michael A. Anderson project ownership metadata.

## Current Benchmark

- Rows: `250`.
- Average token savings vs broad-context baseline: `0.9500`.
- Wrong high-confidence: `0`.
- Unsupported high-confidence: `0`.
- Nonpreferred model used: `false`.

## Install

```bash
git clone https://github.com/mikeanderson42/TopoAccess.git
cd TopoAccess
python -m pip install -e packages/topoaccess_prod
topoaccessctl --help
```

## Use With Harnesses

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief \
  --profile default \
  --task "Plan a safe repo change"
```

HTTP, stdio, OpenAPI, and MCP-like schemas are included under `release/topoaccess_prod_v41/`.

## Safety

- Model-agnostic by default.
- Exact lookup never requires a model.
- Public CI does not require model weights, GPU, LM Studio, Ollama, or private caches.
- Local model adapters are configured by workspace profile.
- Provenance is required for audited answers.

Qwen3.6-35B-A3B-uncensored-heretic-APEX-I-Compact was used for local validation only and is not a public dependency.

## Checks Passed

- Product tests: `67 passed`.
- Compileall: passed.
- Editable install: passed.
- CLI help: passed.
- Artifact audit: `0` failures.
- Secret scan: `0` failures.
- Conformance: `8` checks, `0` failures.
