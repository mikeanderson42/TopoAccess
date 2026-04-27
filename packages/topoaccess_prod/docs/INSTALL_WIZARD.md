# Install Wizard

The install wizard detects repo, cache, preferred-model search artifacts, Python, and workspace profile readiness.

Run:

```bash
python packages/topoaccess_prod/scripts/topoaccess_install_wizard.py --profile default --repo . --cache cache/topoaccess_v21 --preferred-search runs/topoaccess_v22/preferred_model_search.jsonl --dry-run
```

The wizard prints next commands and never edits shell profiles unless an explicit future apply mode is added.

