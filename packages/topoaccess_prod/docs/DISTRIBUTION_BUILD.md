# Distribution Build

V38 builds TopoAccess as a Python distribution when local build tooling is available.

If `python -m build` is unavailable, the build tool creates a safe fallback source archive containing only the product package, docs, configs, tests, and safe metadata.

```bash
python packages/topoaccess_prod/scripts/topoaccess_build_dist.py --package packages/topoaccess_prod --out release/topoaccess_prod_v38/dist
```

