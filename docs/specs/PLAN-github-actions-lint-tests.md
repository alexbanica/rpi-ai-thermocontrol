# Plan: GitHub Actions Lint and Test Repair

Status: Approved

## Spec Reference

- `docs/specs/SPEC-github-actions-lint-tests.md`
- Status: Approved

## Affected Files

- `ruff.toml`
- `tests/test_thermo_control_service.py`
- `docs/specs/SPEC-github-actions-lint-tests.md`
- `docs/specs/PLAN-github-actions-lint-tests.md`

## Implementation Steps Performed

1. Inspected the latest failed public GitHub Actions run and confirmed that
   dependency installation succeeded before the lint and test commands failed.
2. Reproduced the Ruff failure with Ruff 0.16.3 and identified 27 findings from
   the tool's broad unconfigured defaults.
3. Confirmed the test suite passes on Python 3.10 and identified the two
   Python 3.10-only `float | None` test annotations that prevent Python 3.9
   collection.
4. Added repository Ruff configuration selecting the core lint rules and the
   Python 3.9 target.
5. Replaced the incompatible test-only annotations with `Optional[float]`.
6. Ran the short validation permitted by the `super-agent` workflow.

## Validation Run

- `/tmp/rpi-ai-thermocontrol-ci-tools/bin/ruff check .` passed with Ruff
  0.16.3.
- `PYENV_VERSION=3.10.14 python -m pytest -q` passed: 22 tests.
- `git diff --check` passed.

## Validation Skipped

- Python 3.9 was not installed locally, so the exact hosted interpreter was not
  executed.
- The GitHub Actions workflow was not rerun because no commit or push was
  authorized.
- Longer build, package-publish, and live Forgejo checks were not relevant to
  the failing lint and test gates and exceed this workflow's short-validation
  boundary.

## QA and Review

- QA skipped as required by `super-agent`.
- Independent code review skipped as required by `super-agent`.

## Documentation Updates

- Added the auto-approved completed-work spec and plan only.

## Staging Status

- All four accepted in-scope paths were staged after final validation and diff
  reconciliation.

## Commit and Push Status

- Commit not authorized and not performed.
- Push not authorized and not performed.

## Residual Risk

- The repaired revision must be committed and pushed before GitHub-hosted
  Python 3.9 can confirm both gates.
- The lint baseline is intentionally limited to core Ruff checks; broader
  policy requires a separate scoped change.
