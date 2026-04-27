# TopoAccess V40 Candidate

## Result

PR #1 is merged and `main` was verified.

PR: https://github.com/mikeanderson42/TopoAccess/pull/1

Main commit: `e303c4f`

## Answers

- Is PR #1 merged? Yes.
- Are files visible on main? Yes.
- Did tests pass? Yes, `67 passed`.
- Did install smoke pass? Yes.
- Did audit/scan/conformance pass? Yes: audit `0`, secret scan `0`, conformance `8/8`.
- Is README public-ready? Improved for model-agnostic positioning and install UX.
- Were release assets created? Yes, under `release/topoaccess_prod_v40/`.
- Was GitHub release created? No. It is prepared only; release creation should happen after the V40 assets/docs PR is merged.

## Model-Agnostic Public Cleanup

Public wording now states:

- TopoAccess is model-agnostic by default.
- Model-backed synthesis is optional and workspace-configured.
- Exact lookup never requires a model.
- Public CI is model-free.
- Qwen was used for local validation only.

## Next Command

Review and merge the V40 release-assets PR after it is opened:

```bash
gh pr view --repo mikeanderson42/TopoAccess --web
```

After that PR is merged, create the prerelease:

```bash
gh release create v1.0.0-rc1 --repo mikeanderson42/TopoAccess --target main --title "TopoAccess v1.0.0-rc1" --notes-file release/topoaccess_prod_v40/release_notes.md --prerelease
```
