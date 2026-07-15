# Plan: Fan Temperature Moving Average

Status: Approved

## Approved Spec

- `docs/specs/fan-temperature-moving-average.md`
- Status: Approved

## Objective

Implement the approved configurable sliding-average fan-control behavior without changing temperature-source selection, control-loop cadence, GPIO adapter behavior, or unrelated runtime behavior.

## No-Research Constraint

Implementation must use only the approved spec, applicable agent instructions, this plan, current branch and worktree state, the files listed or directly implied here, and minimal local edit patterns. It must not reopen product, architecture, scope, or plan research. Any behavior conflict or missing requirement discovered during implementation requires stopping for a spec or plan amendment.

## Architecture and Ownership Boundaries

- `thermocontrol/domain/entities/context_entity.py` owns the configured average read count in the runtime context.
- `thermocontrol/shared/constants.py` owns the YAML key, default value, and any shared validation or logging strings needed by the existing architecture.
- `thermocontrol/infrastructure/parsers/yaml_config_parser.py` owns YAML extraction and strict validation of the configured value.
- `thermocontrol/application/services/thermo_control_service.py` owns the in-memory sliding window, warm-up state, arithmetic mean, fan decision, and decision-average transition logging.
- Infrastructure temperature and GPIO services remain unchanged unless an approved-plan conflict is identified.
- `tests/test_yaml_config_parser.py` and `tests/test_thermo_control_service.py` own deterministic parser and use-case regression coverage.
- `resources/config.yml`, `README.md`, and `AGENTS.md` own default configuration, user documentation, and active-spec/branch guidance respectively.
- No HTTP/OpenAPI contract work is applicable.

## Expected Files

- `AGENTS.md`
- `README.md`
- `resources/config.yml`
- `thermocontrol/shared/constants.py`
- `thermocontrol/domain/entities/context_entity.py`
- `thermocontrol/infrastructure/parsers/yaml_config_parser.py`
- `thermocontrol/application/services/thermo_control_service.py`
- `tests/test_yaml_config_parser.py`
- `tests/test_thermo_control_service.py`
- `docs/specs/fan-temperature-moving-average.md`
- `docs/specs/PLAN-fan-temperature-moving-average.md`

Files outside this list may be changed only when directly required by the approved spec and must be called out in the completion report.

## Branch Policy

1. Begin implementation only after the clean-context gate is satisfied.
2. Confirm the worktree still contains only the approved spec and plan changes plus any explicitly acknowledged user changes.
3. The current and expected base branch is `main` at `origin/main` commit `b3b5cbf` as observed during planning.
4. Create and switch to `spec/fan-temperature-moving-average` from that base while preserving the approved uncommitted artifacts.
5. If `main` or `origin/main` has moved, the current branch differs, or unrelated worktree changes appear, stop and ask before branch creation.
6. Workers must not create branches, commit, or push.

## Test-First Phase

Use one clean-context test-focused subagent with the `gpt-5.3-codex-spark` model before production implementation. Give it only the approved artifacts, applicable instructions, exact test ownership, and minimal existing test context.

The test-focused worker must update deterministic tests before production code for:

1. Explicit and default `temperature_average_read_count` parsing.
2. Rejection of booleans, zero, negative values, floats, strings, and null as invalid configured values.
3. No fan enablement before a full valid window.
4. The first decision when the final warm-up sample fills the window.
5. Sliding eviction of the oldest measurement.
6. Averages above, below, and exactly equal to the threshold.
7. The fan remaining enabled across consecutive averages at or above the threshold.
8. An unavailable read forcing off without entering or clearing the retained valid window, followed by recovery.
9. Transition logging using the unrounded decision average and configured threshold, with no transition logs during warm-up.

The worker must not edit production files. If it reaches five minutes, interrupt it, preserve usable tests, split remaining deterministic coverage, and continue with a different clean-context test-focused worker, one subtask at a time.

## Production Implementation

Use no more than one active clean-context implementation worker with the `gpt-5.3-codex-spark` model. This is a small, coupled behavior change and does not require production subtask splitting unless the worker approaches the five-minute limit.

Ordered work:

1. Add the shared YAML key and default read count of `5`.
2. Add the average read count to `ContextEntity` using the shared default.
3. Parse the optional AI-module configuration value and reject every invalid category defined by the spec, allowing the startup controller's existing exception path to return failure.
4. Add a bounded in-memory collection to `ThermoControlService`, sized from the validated context value.
5. On valid reads, append the measurement; keep the fan off during incomplete-window warm-up; and calculate the unrounded arithmetic mean once full.
6. Make both enable and disable threshold decisions from the full-window average while preserving `>=` equality behavior.
7. On unavailable reads, request fan off, retain the existing valid window, and avoid adding a value or emitting a numeric average-based transition log.
8. Pass the decision average to existing valid transition logging without changing message formats or repeated same-state behavior.
9. Make the production code pass the test-first coverage without changing tests merely to accommodate an incorrect implementation.

The implementation worker must not edit documentation, specs, the plan, branch state, commits, or pushes. If implementation exposes a spec conflict or materially different behavior, stop rather than infer a solution.

## Main-Agent Review and Fix Flow

1. The main agent inspects the worker diff for ownership, architecture direction, unnecessary changes, and agreement with every approved requirement.
2. Use one clean-context code-review subagent at a time with the approved artifacts and focused diff. The reviewer must check spec and plan conformance, boundary cases, missing tests, deterministic behavior, regressions, and architecture violations without editing files.
3. If review is likely to exceed five minutes, split it into smaller synchronous review assignments and use a different clean-context reviewer after interruption.
4. Route confirmed in-scope findings to a new clean-context implementation worker using the required model, exact finding, allowed ownership boundary, and relevant minimal context.
5. The main agent performs final acceptance after fixes and reruns proportionate validation.

## Documentation and Configuration

After production behavior passes focused tests, the main agent must:

1. Add `temperature_average_read_count: 5` under `thermocontrol.ai_module` in `resources/config.yml`.
2. Update the README YAML example and describe the default, valid range, full-window startup delay, `check_interval` measurement cadence, failed-read behavior, and decision-average transition logging.
3. Update `AGENTS.md` so the active spec and branch identify this work, without changing architecture rules.
4. Keep the approved spec and plan synchronized only for status or factual path metadata; behavior changes require renewed approval.

## Validation and Main-Agent QA

Run these commands sequentially from the repository root:

1. `pytest`
2. `ruff check .`
3. `python3 -m compileall thermocontrol tests`
4. `git diff --check`

The main agent additionally reviews test evidence and manually traces these sequences against toggle calls and logs:

- Default five-read warm-up followed by an above-threshold average.
- A full sliding window crossing from above to below threshold and back.
- Exact threshold equality.
- A temporary unavailable read while the fan is enabled, followed by a valid recovery read using retained samples.
- Invalid configuration causing startup failure rather than fallback or coercion.

No hardware GPIO or live hwmon validation is required because the approved behavior is deterministic application/configuration logic behind existing interfaces. Any validation not run or not passing must be reported and makes delivery draft.

## Commit and Push Policy

1. After tests, review, QA, documentation, and final acceptance pass, stage only the approved in-scope files.
2. Commit using `feature: Add temperature averaging to fan control`.
3. Push `spec/fan-temperature-moving-average` to `origin`.
4. Do not open a pull request unless the user requests one.
5. If any required validation, review, QA, or documentation is skipped, blocked, incomplete, or failing, use a `DRAFT` commit only if preserving/pushing work is necessary and report delivery as draft.

## Completion Report Requirements

The final implementation report must state the implemented behavior, review and QA issues found, findings resolved, validation run and not run, remaining risks, documentation updates, commit and push status, final or draft delivery status, skipped or blocked requirements, Definition of Done status, and confirmation of final main-agent acceptance.
