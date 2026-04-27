# TopoAccess V41 Release

## Assets

- `release/topoaccess_prod_v41/dist/topoaccess_prod_v41-source-fallback.tar.gz`
- `release/topoaccess_prod_v41/archive/topoaccess_prod_v41-release.tar.gz`
- `release/topoaccess_prod_v41/checksums.txt`
- `release/topoaccess_prod_v41/release_manifest.json`
- `release/topoaccess_prod_v41/release_notes.md`
- `release/topoaccess_prod_v41/upload_commands.md`

## Gates

- Product tests: `67 passed`.
- Compileall: passed.
- Editable install: passed.
- CLI help: passed.
- Artifact audit: `351` files, `0` failures.
- Secret scan: `351` files, `0` failures.
- Conformance: `8` rows, `0` failures.

## Release Status

GitHub release assets were prepared but not uploaded. The release should be created only after this PR is merged and checks are green on `main`.

## Commands

```bash
gh release create v1.0.0-rc1 --repo mikeanderson42/TopoAccess --target main --title "TopoAccess v1.0.0-rc1" --notes-file release/topoaccess_prod_v41/release_notes.md --prerelease
```

```bash
gh release upload v1.0.0-rc1 --repo mikeanderson42/TopoAccess release/topoaccess_prod_v41/dist/topoaccess_prod_v41-source-fallback.tar.gz release/topoaccess_prod_v41/archive/topoaccess_prod_v41-release.tar.gz release/topoaccess_prod_v41/checksums.txt release/topoaccess_prod_v41/release_manifest.json
```
