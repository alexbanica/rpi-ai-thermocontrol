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

1. Replaced the regex-looking GitHub tag filter with an all-tag glob, leaving
   exact acceptance to the shell validator.
2. Added stable and beta tag parsing, including beta-to-PEP-440 conversion.
3. Compared the parsed `setup.py` version and verified the downloaded package
   against the derived package version.
4. Set `setup.py` to the existing stable release version, `1.0.0`.
5. Recorded this completed-work specification and plan.

## Validation run

- Local stable, beta, and invalid-tag parser simulations.
- `git diff --check`.

## Validation skipped

- Full test suite, hosted workflow rerun, and live Forgejo publication.

## QA and code review

QA and code review were skipped as required by `$super-agent`.

## Staging and delivery status

All accepted in-scope paths are staged. No commit or push is performed because
the user did not request either.

## Residual risk

Hosted Actions behavior and the Forgejo registry's beta-version normalization
remain unverified until a matching beta package is published.
