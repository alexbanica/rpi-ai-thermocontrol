# Spec: Fan Toggle Temperature Logging

## Purpose
Add deterministic fan toggle logging that records the measured temperature from the hwmon source used for the control decision.

## Definitions
- Toggle event: A fan state transition only (`OFF -> ON` or `ON -> OFF`).
- Determination cycle: A control-loop iteration that reads temperature and computes desired fan state.
- Decision temperature: The temperature value returned by the readable hwmon source selected by the temperature reader for that cycle.

## Scope
- Emit one log line when fan transitions `OFF -> ON`.
- Emit one log line when fan transitions `ON -> OFF`.
- Include the decision temperature in the toggle log message.
- Keep current warning behavior when no configured hwmon temperature can be read.

## Non-Goals
- Logging on every determination cycle when no fan transition occurred.
- Aggregating or logging all hwmon source values.
- Changing fan control threshold logic.

## Invariants
- Toggle logging is emitted only for state transitions, never for repeated same-state commands.
- Logged temperature must correspond to the device reading used in that same cycle's control decision.
- If `hwmon1` is the source selected for the cycle, the logged value is the `hwmon1` reading.
- If no hwmon source is readable, fan remains `OFF` and warning log indicates temperature cannot be read.

## Constraints
- Use existing logging framework and standard level conventions.
- `OFF -> ON` log level is `INFO`.
- `ON -> OFF` log level is `INFO`.
- Message format:
  - `Fan enabled at temperature=<value_celsius>C`
  - `Fan disabled at temperature=<value_celsius>C`

## Assumptions
- Temperature read always precedes fan state decision in each control cycle.
- Fan can only be enabled when a valid decision temperature is available.

## Implementation Plan
1. Ensure control flow can detect previous and next fan state to identify transitions.
2. Reuse cycle decision temperature in transition log emission.
3. Keep existing unreadable-temperature warning behavior and forced-`OFF` behavior unchanged.
4. Add/adjust tests to validate:
   - `OFF -> ON` logs once with decision temperature.
   - `ON -> OFF` logs once with decision temperature.
   - No transition produces no toggle log.
   - Unreadable temperature keeps fan `OFF` and emits warning.

## Regression Analysis
Potential regressions:
- Duplicate logs caused by logging each loop rather than on transitions.
- Incorrect temperature source in message when multiple hwmon entries exist.
- Behavior drift when temperature is unreadable.

Mitigations:
- Add transition-focused unit tests with previous/next state assertions.
- Add multi-hwmon tests to verify reported value matches selected source.
- Keep and validate unreadable-temperature warning and `OFF` fallback.
