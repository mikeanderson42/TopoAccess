# TopoAccess

TopoAccess is a local repo-intelligence sidecar for coding agents.

It is not a replacement for Codex, Claude Code, Cursor, Aider, OpenClaw, OpenHands, or other coding agents. It gives those agents a smaller, provenance-backed view of a repository so exact lookup, test-impact, command lookup, change planning, and post-edit validation do not require dumping broad repo context into a model.

## Why It Exists

Coding agents waste tokens and make mistakes when they must rediscover repository structure from scratch. TopoAccess routes exact work through deterministic tools and TopoGraph/cache indexes, then reserves model use for category-gated synthesis tasks.

Measured local release-candidate results:

- Codex dogfood savings: 0.9332 average token savings over 250 V38 tasks.
- Harness token savings baseline: 0.9553.
- Exact lookup: tool-only.
- Preferred model use: category-gated.
- Wrong high-confidence: 0.
- Unsupported high-confidence: 0.

Public CI does not require a local Qwen model, GPU, LM Studio, Ollama, private cache, or model weights.

## Architecture

```text
coding agent -> TopoAccess CLI/HTTP/stdio -> router -> deterministic tools / TopoGraph / cache
                                             -> category-gated preferred model only when allowed
                                             -> provenance + trace + safety counters
```

## Install

```bash
git clone https://github.com/mikeanderson42/TopoAccess.git
cd TopoAccess
python -m pip install -e packages/topoaccess_prod
topoaccessctl --help
```

## Quick Start

```bash
python packages/topoaccess_prod/scripts/topoaccessctl.py status --cache cache/topoaccess_v21
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief --profile default --task "Improve exact command lookup resolver"
python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile default --changed-files packages/topoaccess_prod/README.md
```

## Harness Integrations

- Codex: `release/topoaccess_prod_v37/AGENTS.md` style guidance and `topoaccess_agent.py codex-brief`.
- Claude Code: safe hook examples.
- Cursor: `.mdc` rules.
- Aider: token-budgeted repo-map export.
- Hermes/generic: CLI/HTTP/stdio tool schemas.

## Safety Model

- Exact lookup remains tool-only.
- Model use remains category-gated for change planning, model-required narrative, report synthesis, and troubleshooting.
- Nonpreferred model use fails local release gates.
- Provenance is required for audited answers.
- Unsupported requests should abstain instead of guessing.

## Known Limitations

- Native service install remains an operator action.
- Public CI is model-free and validates import, CLI, tests, conformance, artifact audit, and secret scan.
- Local model-backed categories require operator configuration.

## License And Credits

Apache-2.0. Creator / Project Owner / System Architect: Michael A. Anderson <MikeAnderson42@gmail.com>.

AI-assisted implementation is credited as assistance under Michael A. Anderson's direction, not ownership.
