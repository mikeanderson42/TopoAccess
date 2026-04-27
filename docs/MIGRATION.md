# Migrating To `topoaccess`

The short `topoaccess` command is now the preferred public interface. Existing commands are preserved.

| Old command | Preferred command |
| --- | --- |
| `python packages/topoaccess_prod/scripts/topoaccess_workspace.py init --profile demo --repo . --cache .topoaccess/cache` | `topoaccess workspace init --profile demo --repo . --cache .topoaccess/cache` |
| `python packages/topoaccess_prod/scripts/topoaccess_doctor.py --profile demo` | `topoaccess doctor --profile demo` |
| `python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief --profile demo --task "..."` | `topoaccess codex-brief --profile demo --task "..."` |
| `python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile demo --changed-files README.md` | `topoaccess post-edit --profile demo --changed-files README.md` |
| `python packages/topoaccess_prod/scripts/topoaccess_conformance_check.py --release examples/integrations` | `topoaccess conformance --release examples/integrations` |
| `python packages/topoaccess_prod/scripts/topoaccess_artifact_audit.py --paths packages/topoaccess_prod README.md docs examples` | `topoaccess audit --paths packages/topoaccess_prod README.md docs examples` |
| `python packages/topoaccess_prod/scripts/topoaccess_secret_scan.py --paths packages/topoaccess_prod README.md docs examples` | `topoaccess secret-scan --paths packages/topoaccess_prod README.md docs examples` |

Use legacy script paths when debugging packaging or when a harness calls a specific script path. They are not deprecated for compatibility, but public docs should prefer `topoaccess`.
