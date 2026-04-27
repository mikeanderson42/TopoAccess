# TopoAccess Commands

`topoaccess` is the primary public command. `topoaccessctl` and the legacy `packages/topoaccess_prod/scripts/*.py` entrypoints remain available for compatibility and advanced workflows.

## Core

```bash
topoaccess --help
topoaccess version
topoaccess commands
topoaccessctl --help
```

## Workspace

```bash
topoaccess workspace init --profile demo --repo . --cache .topoaccess/cache
topoaccess workspace status --profile demo
topoaccess workspace list
topoaccess workspace validate --profile demo
topoaccess doctor --profile demo
topoaccess doctor --fix-suggestions --profile demo
```

## Agent Workflows

```bash
topoaccess codex-brief --profile demo --task "What tests should I run after editing README.md?"
topoaccess preflight --profile demo --task "Plan a safe CLI improvement"
topoaccess post-edit --profile demo --changed-files README.md docs/QUICKSTART.md
topoaccess query --profile demo --query "Where is the CLI entrypoint?" --why --audit
```

## Benchmarks

```bash
topoaccess benchmark smoke --profile demo
topoaccess benchmark scenario --profile demo --scenarios 50
```

## Integrations

```bash
topoaccess serve-http --profile demo --port 8876 --smoke
topoaccess stdio --profile demo --help
topoaccess install-harness --target codex --profile demo --dry-run
```

`topoaccess serve-http` without `--smoke` and `topoaccess stdio` are long-running integration processes.

## Validation

```bash
topoaccess self-check --profile demo
topoaccess conformance --release examples/integrations
topoaccess audit --paths packages/topoaccess_prod README.md docs examples
topoaccess secret-scan --paths packages/topoaccess_prod README.md docs examples
```

All public commands are model-free by default. Exact lookup remains tool-only. Optional model-backed synthesis is configured by workspace profile and remains category-gated.
