# Spec: GitHub Actions Lint and Test Repair

Status: Approved

## Purpose

Restore the existing GitHub Actions `Lint` and `Tests` gates on Python 3.9
without changing application runtime behavior.

## Requested Behavior

- `ruff check .` succeeds against an explicit, repository-owned lint contract.
- `pytest` can collect and run the test suite on the package's declared minimum
  Python version, Python 3.9.
- The repair does not change the workflow triggers, publishing behavior,
  application services, hardware adapters, or runtime dependencies.

## Scope

- Add repository Ruff configuration.
- Make the incompatible test-only union annotations valid on Python 3.9.
- Preserve the existing workflow commands and Python version.

## Out of Scope

- Refactoring pre-existing runtime logging or exception handling.
- Expanding lint to optional Ruff rule families.
- Changing package metadata, supported Python versions, or release behavior.
- Committing, pushing, or rerunning GitHub Actions.

## Inputs and Constraints

- The failing run is GitHub Actions run `32017266716` at commit
  `483a90cfe118dc322f411b5be79e0473244ed07d`.
- Dependency installation succeeded in both jobs. `ruff check .` exited with
  status 1 and `pytest` exited with status 2 during collection.
- The workflow and `setup.py` require Python 3.9.
- Current Ruff 0.16.3 reports 27 pre-existing findings when no repository
  configuration defines a target or selected rules. Some findings recommend
  Python 3.10-only annotation syntax, which conflicts with Python 3.9 support.

## Deterministic Behavior Delivered

- `ruff.toml` sets `target-version = "py39"`.
- Ruff selects the stable core `E4`, `E7`, `E9`, and `F` rule families, making
  `ruff check .` independent of future default-rule expansion.
- `FakeTemperatureService` uses `typing.Optional` instead of runtime-evaluated
  `float | None`, so importing the test module does not require Python 3.10.
- Production code and behavior remain unchanged.

## Assumptions

- The original unconfigured Ruff invocation was intended to provide core
  syntax, import, and undefined-name checks rather than mandate a broad runtime
  refactor.
- Python 3.9 remains the minimum supported and CI validation version.

## Impact

- Hosted lint and test jobs should pass for the repaired source revision.
- The test suite remains semantically unchanged.
- Additional lint policies can be introduced separately and intentionally.

## Validation Performed

- Ruff 0.16.3: `ruff check .` passed.
- Python 3.10.14: `python -m pytest -q` passed all 22 tests.
- `git diff --check` passed.

## Validation Skipped

- Local Python 3.9 execution was unavailable.
- GitHub Actions was not rerun because this `super-agent` invocation does not
  commit or push.
- QA and independent code review were skipped by the `super-agent` workflow.

## Documentation Changes

- Added this completed-work spec and its matching completed-work plan.
- No operator or user documentation changed because runtime and release usage
  are unchanged.
