# TopoAccess V40 Release

Release assets were prepared but no GitHub Release was created or uploaded.

## Assets

- `release/topoaccess_prod_v40/dist/topoaccess-prod-v38-source-fallback.tar.gz`
- `release/topoaccess_prod_v40/archive/topoaccess-prod-v38-release.tar.gz`
- `release/topoaccess_prod_v40/checksums.txt`
- `release/topoaccess_prod_v40/release_notes.md`
- `release/topoaccess_prod_v40/upload_commands.md`
- `release/topoaccess_prod_v40/release_manifest.json`

## Gates

- Product tests: `67 passed`.
- Install smoke: passed.
- Artifact audit: `0` failures.
- Secret scan: `0` failures.
- Conformance: `8` rows, `0` failures.

## Release Command

After the V40 release-assets PR is merged:

```bash
gh release create v1.0.0-rc1 --repo mikeanderson42/TopoAccess --target main --title "TopoAccess v1.0.0-rc1" --notes-file release/topoaccess_prod_v40/release_notes.md --prerelease
```

Then upload the audited assets listed in `release/topoaccess_prod_v40/upload_commands.md`.
