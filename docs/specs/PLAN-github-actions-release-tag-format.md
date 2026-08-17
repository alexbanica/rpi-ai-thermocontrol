# GitHub Actions release tag format plan

Status: Approved

## Spec reference

`docs/specs/SPEC-github-actions-release-tag-format.md`

## Affected files

- `.github/workflows/ci-publish.yml`
- `setup.py`
- `docs/specs/SPEC-github-actions-release-tag-format.md`
- `docs/specs/PLAN-github-actions-release-tag-format.md`

## Implementation performed

1. Matched the receiver's numeric stable/beta tag trigger patterns while
   retaining exact shell validation.
2. Added stable and beta tag parsing, including beta-to-PEP-440 conversion.
3. Removed the static package-version comparison and the `main`-ancestry gate.
4. Passed the tag-derived version to the release build through
   `RELEASE_VERSION`, which `setup.py` uses without changing local defaults.
5. Verified downloads against that same tag-derived package version.
6. Disabled build isolation only for the anonymous source-distribution download
   so pip does not request build dependencies from Forgejo's package index.
7. Recorded this completed-work specification and plan.

## Validation run

- Local stable, beta, and invalid-tag parser simulations; default/injected
  `setup.py` version checks; pip option check.
- `git diff --check`.

## Validation skipped

- Full test suite, hosted workflow rerun, and live Forgejo publication.

## QA and code review

QA and code review were skipped as required by `$super-agent`.

## Staging and delivery status

All accepted in-scope paths are staged. No commit or push is performed because
the user did not request either.

## Residual risk

Hosted Actions behavior, tag checkout, and Forgejo publication/download remain
unverified until a tag is recreated on the delivered workflow commit.
