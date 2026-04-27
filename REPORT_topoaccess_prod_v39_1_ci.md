# TopoAccess V39.1 CI

## Root Cause

The public PR branch had a broad `.gitignore` rule for `cache/`, which ignored `packages/topoaccess_prod/topoaccess_prod/cache/`. GitHub Actions then failed on:

```text
ModuleNotFoundError: No module named 'topoaccess_prod.cache'
```

## Fix

- Narrowed `.gitignore` from `cache/` to `/cache/`.
- Explicitly unignored `packages/topoaccess_prod/topoaccess_prod/cache/`.
- Added public `topoaccess_prod.cache` modules.
- Added missing-cache and fixture-cache tests.

## Local Checks

- `python -m pytest packages/topoaccess_prod/tests/test_product_cache.py`: 3 passed.
- `python -m pytest packages/topoaccess_prod/tests`: 67 passed.
- `python packages/topoaccess_prod/scripts/topoaccess_ci_local.py ...`: passed.
- `python -m compileall .`: passed.
- `python -m pip install -e packages/topoaccess_prod`: passed.
- `topoaccessctl --help`: passed.
- Conformance: 8 rows, 0 failures.

Public CI remains model-free and cache-free.
