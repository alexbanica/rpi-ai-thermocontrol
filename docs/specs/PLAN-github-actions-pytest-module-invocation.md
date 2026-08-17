# GitHub Actions pytest module invocation plan

Status: Approved

## Spec reference

`docs/specs/SPEC-github-actions-pytest-module-invocation.md`

## Affected files

- `.github/workflows/ci-publish.yml`
- `docs/specs/SPEC-github-actions-pytest-module-invocation.md`
- `docs/specs/PLAN-github-actions-pytest-module-invocation.md`

## Implementation performed

1. Retrieved and inspected the failed GitHub Actions job log.
2. Confirmed test collection failed because `thermocontrol` was absent from the
   console-script process import path.
3. Replaced `pytest` with `python -m pytest` in the Tests job.
4. Recorded this completed-work spec and plan.

## Validation run

- GitHub job-log inspection.
- Workflow command syntax inspection.
- `git diff --check` is run after this artifact is created.

## Validation skipped

Local pytest execution and a hosted workflow rerun were not run. Installing
dependencies is expected to exceed the `$super-agent` ten-second validation
limit.

## QA and code review

QA and code review were skipped as required by `$super-agent`.

## Documentation updates

The completed-work spec and this plan document the repair and its validation
limits.

## Delivery status

All accepted in-scope paths are staged. No commit or push is performed because
the user did not request either.

## Residual risk

The fix is based on the exact hosted failure log but remains unverified by a
new hosted run.
