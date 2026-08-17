# GitHub Actions package-version validation plan

Status: Approved

## Spec reference

`docs/specs/SPEC-github-actions-package-version-validation.md`

## Affected files

- `.github/workflows/ci-publish.yml`
- `docs/specs/SPEC-github-actions-package-version-validation.md`
- `docs/specs/PLAN-github-actions-package-version-validation.md`

## Implementation performed

1. Inspected the failed release-job metadata and local workflow command.
2. Identified that unconditional `sys.exit(0)` prevented Python from printing
   the matched package version.
3. Changed the expression to print the match or exit only when it is absent.
4. Recorded this completed-work spec and plan.

## Validation run

- Local version-extraction simulation.
- `git diff --check`.

## Validation skipped

- Full test suite, hosted workflow rerun, and live Forgejo publication.

## QA and code review

QA and code review were skipped as required by `$super-agent`.

## Staging and delivery status

All accepted in-scope paths are staged. No commit or push is performed because
the user did not request either.

## Residual risk

The repair has not yet been exercised by GitHub Actions or a live package
publication.
