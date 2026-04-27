# TopoAccess V41 Repo Cleanup

## Public Surface Audit

The public repo contained current source/tests/docs plus internal version clutter from prior release-candidate preparation:

- root `REPORT_topoaccess_prod_v39_1_*.md`
- root `REPORT_topoaccess_prod_v40_*.md`
- old `release/topoaccess_prod_v32`
- old `release/topoaccess_prod_v33`
- old `release/topoaccess_prod_v39`
- old `release/topoaccess_prod_v39_1`
- old `release/topoaccess_prod_v40`

## Cleanup Decision

The public surface should focus on the current product:

- `README.md`
- Apache-2.0 license and project metadata
- `docs/`
- `examples/`
- `packages/topoaccess_prod/`
- `.github/`
- current `release/topoaccess_prod_v41/`

Useful current harness/conformance artifacts were copied into `release/topoaccess_prod_v41/`. Old reports and old release folders were removed from the public surface rather than kept at the root.

## History

Added `docs/history/DEVELOPMENT_HISTORY.md` as a concise historical note without exposing old internal candidate reports as top-level public files.

No source, tests, docs, examples, CI, license, or owner metadata files were deleted.
