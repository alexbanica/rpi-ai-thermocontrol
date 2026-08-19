# Persist Fan-Off State After Shutdown Plan

Status: Approved

## Spec Reference

- `specs/SPEC-persist-fan-off-after-shutdown.md`

## Affected Files

- `thermocontrol/infrastructure/services/rpi_service.py`
- `thermocontrol/shared/constants.py`
- `specs/SPEC-persist-fan-off-after-shutdown.md`
- `specs/PLAN-persist-fan-off-after-shutdown.md`

## Implementation Steps Performed

1. Traced fan shutdown through the application service, GPIO adapter, and GPIO
   Zero `lgpio` cleanup behavior.
2. Replaced deletion and a fixed sleep with explicit output-device and pin
   factory closure.
3. Added an idempotent post-release operation that invokes Raspberry Pi
   `pinctrl` with an argument list to leave the configured GPIO output low.
4. Added success and failure diagnostics for the post-release state.
5. Recorded the graceful-shutdown, platform, and electrical boundaries.

## Validation Run

- Python compilation of changed modules.
- `git diff --check`.

## Validation Skipped

- Live GPIO/fan validation because Raspberry Pi hardware is unavailable in this
  workspace.
- Ruff static checking because Ruff is not installed in this checkout.
- Automated infrastructure tests because project policy permits automated tests
  only for deterministic domain source logic.

## QA And Code Review

- QA skipped by the `super-agent` workflow.
- Code review skipped by the `super-agent` workflow.

## Documentation Updates

- Added the completed spec and plan; no operator README was changed because it
  already contains unrelated user edits.

## Staging Status

- All accepted in-scope paths are staged after validation and reconciliation.

## Commit And Push Status

- The user explicitly authorized committing these in-scope changes and pushing
  them directly to `origin/main` in a follow-up request.
- Delivery starts from the freshly fetched `origin/main` commit
  `b4004244c578d567dd8a1fcf290896e4683859cc`.
- The final completion report records the resulting commit and verified remote
  synchronization status.

## Residual Risk

- Live hardware behavior is unverified.
- Persistent output-low behavior requires `pinctrl` and sufficient privilege.
- Only external electrical bias, such as an appropriate pull-down resistor, can
  provide a fail-safe when the software path cannot run.
