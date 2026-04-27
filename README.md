# TopoAccess

TopoAccess is a local repo-intelligence sidecar for coding agents.

It helps tools like Codex, Claude Code, Cursor, Aider, OpenClaw, OpenHands, Hermes/generic agents, HTTP clients, and stdio tools ask better questions about a repository before editing it. It is not a replacement for coding agents. It gives them a compact, provenance-backed repo view so exact lookup, test-impact, command lookup, change planning, and post-edit validation do not require dumping broad repository context into a model.

## Why Use It

Coding agents are strongest when they have the right context and weakest when they must rediscover repo structure from scratch. TopoAccess reduces that rediscovery cost by routing exact repository work through deterministic tools, TopoGraph/cache indexes, and small prompt packs.

Current public benchmark:

| Metric | Result |
| --- | ---: |
| Isolated row benchmark | `10,000` rows |
| Row benchmark average assisted token savings | `0.9462` |
| Row benchmark median assisted token savings | `0.9531` |
| Scenario benchmark | `2,500` workflows / `44,443` steps |
| Scenario benchmark average assisted token savings | `0.9307` |
| Scenario benchmark median assisted token savings | `0.9397` |
| Scenario p50 / p95 latency across all modes | `167.0 ms` / `1166.0 ms` |
| Assisted post-edit validation pass rate | `1.0000` |
| Wrong high-confidence answers | `0` |
| Unsupported high-confidence answers | `0` |

- Exact lookup: tool-only, no model fallback.
- Public CI and public benchmark: model-free, cache-free, GPU-free, and private-runtime-free.
- Model posture: model-agnostic by default; optional model-backed synthesis is configured per workspace.

## How It Works

```text
coding agent
  -> TopoAccess CLI / HTTP / stdio
  -> workspace profile
  -> TopoGraph + cache + deterministic tools
  -> category router
  -> optional workspace model adapter only for allowed synthesis/planning categories
  -> provenance + trace + safety counters
```

Exact lookups, command lookups, artifact facts, and cached repo facts stay on deterministic tool routes and never require a model. Optional model-backed synthesis is only allowed for category-gated tasks:

- `change_planning`
- `model_required_narrative`
- `report_synthesis`
- `troubleshooting`

TopoAccess was locally validated with this workspace model during development, but it is not a public dependency:

```text
Qwen3.6-35B-A3B-uncensored-heretic-APEX-I-Compact
```

Public CI does not require that model, model weights, LM Studio, Ollama, GPU access, or private cache files. Local model adapters are configured through workspace profiles.

## Install

```bash
git clone https://github.com/mikeanderson42/TopoAccess.git
cd TopoAccess
python -m pip install -e packages/topoaccess_prod
topoaccessctl --help
```

## Quick Start

This path is designed for a fresh clone. It does not require Qwen, LM Studio, Ollama, GPU access, private caches, or model files.

```bash
python packages/topoaccess_prod/scripts/topoaccess_workspace.py init \
  --profile demo \
  --repo . \
  --cache .topoaccess/cache

python packages/topoaccess_prod/scripts/topoaccess_doctor.py --profile demo

python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief \
  --profile demo \
  --task "What tests should I run after editing README.md?"

python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit \
  --profile demo \
  --changed-files packages/topoaccess_prod/README.md
```

For a model-free public smoke test:

```bash
python -m pytest packages/topoaccess_prod/tests
topoaccessctl --help
```

## Harness Integrations

- Codex: generate compact mission briefs with `topoaccess_agent.py codex-brief`.
- Claude Code: use safe hook examples in `examples/integrations/claude_hooks/` for preflight and post-edit validation.
- Cursor: use `examples/integrations/cursor_rules/topoaccess.mdc` for read-first, provenance-required workflows.
- Aider: use token-budgeted repo-map exports.
- OpenClaw/OpenHands/Hermes/generic: use CLI, HTTP, stdio, OpenAPI, or MCP-like schemas from `examples/integrations/schemas/`.

## Safety Model

- Exact lookup remains tool-only.
- Optional model-backed synthesis remains category-gated.
- Provenance is required for audited answers.
- Unsupported requests should abstain instead of guessing.
- Installers and publish helpers default to dry-run/read-only behavior.
- Public CI validates package shape without private local runtime assumptions.
- No hidden writes are required for query, explain, preflight, or post-edit validation.

## Known Limitations

- Native service installation remains operator action; the wrapper/package path is validated.
- External harness behavior depends on installed tool versions.
- Private local caches/models are intentionally not included in this public repo.
- Public CI validates deterministic/package behavior, not private model-backed local runtime quality.

## Documentation

- [Install](docs/INSTALL.md)
- [Quickstart](docs/QUICKSTART.md)
- [How It Works](docs/HOW_IT_WORKS.md)
- [Harness Integration](docs/HARNESS_INTEGRATION.md)
- [Benchmarks](docs/BENCHMARKS.md)
- [Token Savings](docs/TOKEN_SAVINGS.md)
- [Model-Agnostic Design](docs/MODEL_AGNOSTIC.md)
- [FAQ](docs/FAQ.md)
- [Safety](docs/SAFETY.md)
- [API](docs/API.md)
- [Development](docs/DEVELOPMENT.md)
- [Publishing](docs/PUBLISHING.md)

## License And Credits

Apache-2.0.

Creator / Project Owner / System Architect: Michael A. Anderson <MikeAnderson42@gmail.com>.

AI-assisted implementation is credited as implementation assistance under Michael A. Anderson's direction, not ownership.
