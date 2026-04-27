# codex TopoAccess install

Dry-run only by default. No external harness config is modified unless an explicit future `--apply` mode is used.

## Exact command

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent_install.py --target codex --profile default --dry-run
```

## Shell snippet

```bash
alias topoaccess-codex='python packages/topoaccess_prod/scripts/topoaccess_agent.py workspace status --profile default'
```

## Config snippet

```json
{"tool_server": "topoaccess", "profile": "default", "schema": "tool_schema.json", "read_only_default": true}
```

## Safety note

Exact lookup remains tool-only. Preferred model fallback is category-gated. Nonpreferred model use fails release gates.

## Test

```bash
python packages/topoaccess_prod/scripts/topoaccess_adapter_smoke.py --profile default --targets codex --out runs/topoaccess_prod_v33/installer_smoke.jsonl --report REPORT_topoaccess_prod_v33_docs.md
```

## Remove

Delete the shell alias/snippet or remove the generated tool entry from your harness config. This dry-run installer does not write external config files.
