# TopoAccess

TopoAccess is a local repo-intelligence sidecar for coding agents.

It helps tools like Codex, Claude Code, Cursor, Aider, OpenClaw, OpenHands, Hermes/generic agents, HTTP clients, and stdio tools ask better questions about a repository before editing it. It is not a replacement for coding agents. It gives them a compact, provenance-backed repo view so exact lookup, test-impact, command lookup, change planning, and post-edit validation do not require dumping broad repository context into a model.

## Why Use It

Coding agents are strongest when they have the right context and weakest when they must rediscover repo structure from scratch. TopoAccess reduces that rediscovery cost by routing exact repository work through deterministic tools, TopoGraph/cache indexes, and small prompt packs.

Measured local release-candidate results:

- Codex dogfood savings: `0.9332` average token savings across 250 V38 tasks.
- Harness token savings: about `0.9553` average across harness/category checks.
- Exact lookup: tool-only, no model fallback.
- Wrong high-confidence answers: `0`.
- Unsupported high-confidence answers: `0`.
- Public CI: model-free, cache-free, GPU-free, and private-runtime-free.

## How It Works

```text
coding agent
  -> TopoAccess CLI / HTTP / stdio
  -> workspace profile
  -> TopoGraph + cache + deterministic tools
  -> category router
  -> optional preferred model only for allowed synthesis/planning categories
  -> provenance + trace + safety counters
```

Exact lookups, command lookups, artifact facts, and cached repo facts stay on deterministic tool routes. Model use is only allowed for category-gated tasks:

- `change_planning`
- `model_required_narrative`
- `report_synthesis`
- `troubleshooting`

The preferred local model remains configurable for local operators:

```text
Qwen3.6-35B-A3B-uncensored-heretic-APEX-I-Compact
```

Public CI does not require that model, model weights, LM Studio, Ollama, GPU access, or private cache files.

## Install

```bash
git clone https://github.com/mikeanderson42/TopoAccess.git
cd TopoAccess
python -m pip install -e packages/topoaccess_prod
topoaccessctl --help
```

## Quick Start

```bash
python packages/topoaccess_prod/scripts/topoaccess_workspace.py init \
  --profile default \
  --repo . \
  --cache cache/topoaccess_v21 \
  --preferred-search runs/topoaccess_v22/preferred_model_search.jsonl

python packages/topoaccess_prod/scripts/topoaccess_doctor.py --profile default

python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief \
  --profile default \
  --task "Improve exact command lookup resolver"

python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit \
  --profile default \
  --changed-files packages/topoaccess_prod/README.md
```

For a model-free public smoke test:

```bash
python -m pytest packages/topoaccess_prod/tests
topoaccessctl --help
```

## Harness Integrations

- Codex: generate compact mission briefs with `topoaccess_agent.py codex-brief`.
- Claude Code: use safe hook examples for preflight and post-edit validation.
- Cursor: use generated `.mdc` rules for read-first, provenance-required workflows.
- Aider: use token-budgeted repo-map exports.
- OpenClaw/OpenHands/Hermes/generic: use CLI, HTTP, stdio, OpenAPI, or MCP-like schemas.

## Safety Model

- Exact lookup remains tool-only.
- Preferred model use remains category-gated.
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
- [Token Savings](docs/TOKEN_SAVINGS.md)
- [Safety](docs/SAFETY.md)
- [API](docs/API.md)
- [Development](docs/DEVELOPMENT.md)
- [Publishing](docs/PUBLISHING.md)

## License And Credits

Apache-2.0.

Creator / Project Owner / System Architect: Michael A. Anderson <MikeAnderson42@gmail.com>.

AI-assisted implementation is credited as implementation assistance under Michael A. Anderson's direction, not ownership.
