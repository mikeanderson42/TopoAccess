# TopoAccess

TopoAccess is a local repo-intelligence sidecar for coding agents.

It helps tools such as Codex, Claude Code, OpenClaw, Hermes, and generic shell/HTTP/stdio-capable agents find the right files, tests, commands, reports, and provenance before they spend tokens reading the whole repo.

## Why It Exists

Direct model use is good at unconstrained narrative phrasing, but it is weak and expensive for exact repo lookup. TopoAccess keeps exact lookup deterministic and tool-only, then optionally uses a workspace-configured model adapter only for category-gated synthesis/planning/troubleshooting tasks.

Measured V33 canonical results:

- Canonical benchmark rows: `500`.
- Canonical token savings: `0.9526` from the V32/V33 JSONL ledger.
- Real agent soak: `1000` fallback tasks.
- Nonpreferred model used: `false`.
- Wrong high-confidence: `0`.
- Unsupported high-confidence: `0`.

## How It Works

```text
repo + reports + cache + TopoGraph
-> deterministic exact lookup tools
-> compact prompt/context packs
-> optional category-gated model-backed synthesis only where useful
-> provenance-checked answer or safe abstention
-> agent-facing CLI / HTTP / stdio tools
```

TopoAccess is not a replacement for coding agents. It is a repo-intelligence layer that gives agents smaller, safer, provenance-backed context.

## Quick Start

```bash
python packages/topoaccess_prod/scripts/topoaccess_workspace.py init --profile default --repo . --cache cache/topoaccess_v21 --preferred-search runs/topoaccess_v22/preferred_model_search.jsonl
python packages/topoaccess_prod/scripts/topoaccess_doctor.py --profile default --out runs/topoaccess_prod_v33/doctor.jsonl --report REPORT_topoaccess_prod_v33_installers.md
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief --profile default --task "Improve exact command lookup resolver"
```

## Harness Install

Dry-run installers emit snippets and instructions. They do not modify external harness configs by default.

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent_install.py --target codex --profile default --dry-run
python packages/topoaccess_prod/scripts/topoaccess_agent_install.py --target claude-code --profile default --dry-run
python packages/topoaccess_prod/scripts/topoaccess_agent_install.py --target openclaw --profile default --dry-run
python packages/topoaccess_prod/scripts/topoaccess_agent_install.py --target hermes --profile default --dry-run
python packages/topoaccess_prod/scripts/topoaccess_agent_install.py --target generic --profile default --dry-run
```

## Query Examples

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py preflight --profile default --task "Add a token accounting report"
python packages/topoaccess_prod/scripts/topoaccess_agent.py test-impact --profile default --changed-file packages/topoaccess_prod/topoaccess_prod/harness/token_ledger.py
python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile default --changed-files packages/topoaccess_prod/topoaccess_prod/harness/token_ledger.py
```

## Safety Model

- Model posture: model-agnostic by default.
- Local validation model: `Qwen3.6-35B-A3B-uncensored-heretic-APEX-I-Compact`.
- The local validation model is not a required public dependency.
- Nonpreferred model use fails release gates.
- Exact lookup is tool-only.
- Optional model-backed synthesis is category-gated for change planning, model-required narrative, report synthesis, and troubleshooting.
- Unsupported/no-evidence requests abstain.
- Provenance is required for audited answers.

## Limits

Native service installation may remain operator action. The wrapper path is validated.

The harness installers are dry-run by default. Real third-party agent clients should still be tested in their own environments.

## Credits

TopoAccess was created and architected by Michael A. Anderson <MikeAnderson42@gmail.com>. Implementation was AI-assisted with Codex/ChatGPT under Mike’s direction.

## License

Apache-2.0.
