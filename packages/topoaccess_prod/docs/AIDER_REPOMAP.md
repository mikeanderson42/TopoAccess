# Aider Repo Map

TopoAccess can export Aider-style repo maps from the production package surface.

Modes include compact 1k, 2k, and 4k token budgets plus audit JSON. Maps include files, commands, tests, reports, artifacts, and provenance pointers.

Generate:

```bash
python packages/topoaccess_prod/scripts/topoaccess_export_repomap.py --profile default --budgets 1000 2000 4000 --out release/topoaccess_prod_v37/repomap
```

