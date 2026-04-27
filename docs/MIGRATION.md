# Migrating To `topoaccess`

The short `topoaccess` command is now the preferred public interface. Existing commands are preserved.

| Old command | Preferred command |
| --- | --- |
| `python packages/topoaccess_prod/scripts/topoaccess_workspace.py init --profile demo --repo . --cache .topoaccess/cache` | `topoaccess workspace init --profile demo --repo . --cache .topoaccess/cache` |
| First-use workspace setup | `topoaccess init` |
| First-use smoke demo | `topoaccess try` |
| `python packages/topoaccess_prod/scripts/topoaccess_doctor.py --profile demo` | `topoaccess doctor --profile demo` |
| Safe local doctor repairs | `topoaccess doctor --profile demo --fix` |
| `python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief --profile demo --task "..."` | `topoaccess codex-brief --profile demo --task "..."` |
| `python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile demo --changed-files README.md` | `topoaccess post-edit --profile demo --changed-files README.md` |
| `python packages/topoaccess_prod/scripts/topoaccess_conformance_check.py --release examples/integrations` | `topoaccess conformance --release examples/integrations` |
| `python packages/topoaccess_prod/scripts/topoaccess_artifact_audit.py --paths packages/topoaccess_prod README.md docs examples` | `topoaccess audit --paths packages/topoaccess_prod README.md docs examples` |
| `python packages/topoaccess_prod/scripts/topoaccess_secret_scan.py --paths packages/topoaccess_prod README.md docs examples` | `topoaccess secret-scan --paths packages/topoaccess_prod README.md docs examples` |

Use legacy script paths when debugging packaging or when a harness calls a specific script path. They are not deprecated for compatibility, but public docs should prefer `topoaccess`.

Harness setup migration:

```bash
topoaccess setup codex --profile demo --dry-run
topoaccess setup claude --profile demo --dry-run
topoaccess setup cursor --profile demo --dry-run
topoaccess setup openclaw --profile demo --dry-run
topoaccess setup openhands --profile demo --dry-run
```
