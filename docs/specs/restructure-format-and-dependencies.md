# Spec: Restructure, Format, and Dependency Workflow Migration

## Purpose
Restructure the application to a DDD/onion architecture, apply consistent formatting and naming, remove legacy compatibility paths, and adopt split `requirements`-based dependency installation while keeping `setup.py`.

## Definitions
- Domain layer: Pure business entities and service interfaces.
- Application layer: Use-case orchestration and business workflows.
- Infrastructure layer: Hardware and file-system adapters.
- Presentation layer: Runtime entry orchestration.
- Shared layer: Centralized static strings and shared constants.

## Scope
- Refactor package structure to:
  - `thermocontrol/domain`
  - `thermocontrol/application`
  - `thermocontrol/infrastructure`
  - `thermocontrol/presentation`
  - `thermocontrol/shared`
- Remove legacy modules and backward-compatible wrappers.
- Remove empty files and files that contain only imports.
- Keep runtime behavior (temperature read, threshold comparison, GPIO toggle loop, YAML config parsing).
- Add split dependency files:
  - `requirements.txt`
  - `requirements.dev.txt`
  - `requirements/base.txt`
  - `requirements/rpi.txt`
  - `requirements/jetson.txt`
  - `requirements/sunrise_x3.txt`
- Keep `setup.py` and align package discovery to new layout.
- Update `README.md` and `AGENTS.md`.
- Add tests for business logic.

## Non-Goals
- Backward compatibility with previous module paths.
- HTTP/OpenAPI changes (no HTTP API exists).

## Invariants
- Fan is enabled when current temperature is greater than or equal to threshold.
- Fan is disabled otherwise.
- YAML config values override defaults when present.
- Temperature service iterates all configured hwmon entries and uses first readable source.

## Constraints
- DDD/onion dependency direction: outer layers depend inward via interfaces.
- Interface names end with `Interface`.
- Implementations use same base name without `Interface`.
- Static strings are centralized in shared constants.
- LF line endings only.

## Assumptions
- Existing `thermocontrol` package name remains unchanged.
- `pip install .` remains available through `setup.py`.
- Platform-specific GPIO libraries are installed using platform requirement files.

## Implementation Plan
1. Create new architecture modules and migrate logic.
2. Remove obsolete files and import-only package aggregators.
3. Add dependency split files and adjust `setup.py`.
4. Update docs.
5. Add and run tests.
6. Install dependencies with requirements flow in current environment.

## Regression Analysis
Potential regressions:
- Import path breaks due to intentional non-compatibility.
- Packaging issues after moving modules.
- Runtime behavior drift in control loop.

Mitigations:
- Preserve runtime decision logic and defaults.
- Add unit tests for parser and control decision.
- Run test suite and entrypoint check.
