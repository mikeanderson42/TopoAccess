# Branch Protection Guidance

Keep these protections enabled:

- Block force pushes.
- Restrict branch deletions.
- Require a pull request before merging.
- Require status checks to pass before merging.
- Do not bypass failing CI.

For this repository, the required status check should be the actual GitHub check name:

```text
TopoAccess CI / test
```

Do not use the workflow filename as the required check:

```text
.github/workflows/topoaccess-prod-ci.yml
```

GitHub branch rules match status check names, not workflow file paths.

For a solo-maintainer repository, review requirements can block the owner if they are the last pusher. Options:

- Set required approvals to `0` if GitHub rules allow it.
- Use an admin bypass only after CI is green.
- Add a trusted reviewer who can approve the PR.

Do not disable force-push protection, and do not merge while `TopoAccess CI / test` is failing.
