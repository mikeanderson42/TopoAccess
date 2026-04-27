# Distribution

Distribution smoke checks:

- source import,
- script-path CLI help,
- editable install dry-run.

Run:

```bash
python packages/topoaccess_prod/scripts/topoaccess_dist_smoke.py --package packages/topoaccess_prod
python packages/topoaccess_prod/scripts/topoaccess_editable_install_smoke.py --package packages/topoaccess_prod --dry-run-first
```

