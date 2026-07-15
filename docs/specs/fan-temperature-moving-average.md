# Spec: Fan Temperature Moving Average

Status: Approved

## Purpose

Prevent rapid fan state changes caused by individual temperature fluctuations by basing fan control on a configurable sliding average of recent measurements.

## Problem

The service currently compares every temperature measurement directly with the configured threshold. Measurements near the threshold can therefore enable and disable the fan on consecutive control cycles. Fan decisions need to use a recent-temperature average while preserving the existing control interval and unreadable-temperature safety behavior.

## Scope

- Collect one AI-module temperature measurement per determination cycle.
- Calculate a sliding arithmetic mean from a configurable number of the most recent valid measurements.
- Use that average for both fan enable and fan disable decisions.
- Add the AI-module configuration key `temperature_average_read_count`.
- Default `temperature_average_read_count` to `5` when the key is absent.
- Keep the existing `check_interval` as the interval between measurements.
- Report the decision average in valid temperature-driven fan transition logs while retaining the existing log message format.
- Document the new configuration and averaging behavior.

## Out of Scope

- Changing how the hwmon temperature source is selected or read.
- Changing `check_interval` behavior or adding a separate sampling interval.
- Weighted, exponential, time-weighted, or median-based averaging.
- Separate thresholds or hysteresis for enabling and disabling the fan.
- Runtime configuration reloads or changes to the averaging window after startup.
- HTTP, OpenAPI, or `.http` artifacts.

## Definitions

- **Determination cycle:** One control-loop iteration after a `check_interval` wait, during which the service attempts one temperature read and determines the requested fan state.
- **Valid measurement:** A numeric Celsius temperature returned by the configured temperature service. An unavailable reading represented by `None` is not valid.
- **Average read count:** The configured number of valid measurements in the sliding window, provided by `temperature_average_read_count`.
- **Warm-up:** The period after service startup in which fewer valid measurements than the configured average read count have been collected.
- **Decision average:** The unrounded arithmetic mean of all measurements in the full sliding window for the current determination cycle.
- **Full window:** A window containing exactly `temperature_average_read_count` valid measurements.

## Inputs and Constraints

- `temperature_average_read_count` belongs under `thermocontrol.ai_module` in YAML configuration.
- The key is optional and defaults to `5`.
- A configured value must be an integer greater than or equal to `1`.
- Boolean values are invalid even though Python treats booleans as integers.
- Zero, negative, non-integer, and non-numeric values are invalid.
- Invalid configured values must cause configuration parsing and runtime startup to fail; they must not be silently replaced or coerced.
- `check_interval` continues to control the time between attempts to collect consecutive measurements.
- The averaging window exists only in process memory and starts empty whenever the service starts.

## Deterministic Behavior

### Startup and Warm-up

1. The temperature window starts empty.
2. Each valid determination-cycle measurement is appended to the window.
3. While the window contains fewer measurements than `temperature_average_read_count`, the fan must remain off.
4. A partial-window average must not enable the fan.
5. The first threshold-based decision occurs on the cycle that collects the final measurement needed to fill the window.
6. With the default read count of `5`, the first threshold-based decision occurs after five valid measurement cycles. The elapsed time is governed by `check_interval` and the existing loop timing.

### Sliding Average

1. Once full, the window contains only the most recent `temperature_average_read_count` valid measurements.
2. Adding a valid measurement to a full window removes its oldest measurement.
3. The decision average is the arithmetic sum of the window values divided by `temperature_average_read_count`.
4. The average is not rounded before threshold comparison or transition logging.

### Fan Decision

1. When a full window's decision average is greater than or equal to `temperature_threshold`, the fan must be enabled.
2. The fan must remain enabled on every subsequent valid cycle while the decision average remains greater than or equal to the threshold.
3. When a full window's decision average becomes lower than the threshold, the fan must be disabled.
4. At exact equality with the threshold, the fan must remain or become enabled, preserving current comparison behavior.
5. Repeated same-state decisions retain existing fan-control and transition-logging behavior.

### Unavailable Temperature

1. An unavailable temperature must not be added to the averaging window.
2. An unavailable temperature must immediately request the fan off, preserving the existing safety fallback.
3. Previously collected valid measurements remain in the window after an unavailable read.
4. After temperature reading recovers, the next valid measurement resumes the same sliding-window sequence. If the retained window was already full, that cycle can make a new average-based decision immediately.
5. Existing unreadable-temperature warning behavior remains unchanged.

### Transition Logging

1. For a fan transition caused by a valid full-window decision, the value logged as `current_celsius` must be the decision average used for that transition.
2. The threshold in the log must be the configured threshold used for the same decision.
3. Existing transition-only logging and message formats remain unchanged:
   - `Fan enabled at temperature=<current_celsius>/<threshold_celsius>C`
   - `Fan disabled at temperature=<current_celsius>/<threshold_celsius>C`
4. Warm-up cycles must not emit fan-enabled or fan-disabled transition logs.
5. The unavailable-temperature fallback continues to use its existing warning behavior and does not create a numeric average-based transition log.

## Invariants

- Fan threshold decisions use only a full window of valid measurements.
- The window never contains more measurements than the configured average read count.
- Every valid measurement contributes to consecutive sliding windows until it ages out.
- Failed reads never contribute a value to the average.
- The measurement cadence remains controlled solely by `check_interval`.
- The domain and application layers remain independent of YAML, hwmon, GPIO, and process-runtime details.
- The new configuration value follows the existing context and configuration-parser boundaries.

## Assumptions

- Configuration is loaded before the control service is constructed and does not change while it runs.
- Retaining valid measurements across a temporary read failure provides continuity without treating the failure as a temperature value.
- The existing immediate-off fallback on an unavailable temperature remains the desired safety policy.
- Standard floating-point arithmetic is sufficiently precise for the configured Celsius thresholds.

## Regression Impact

Potential regressions include enabling the fan from an incomplete startup window, averaging more or fewer readings than configured, treating failed reads as zero, changing the existing equality boundary, emitting misleading transition temperatures, or altering sampling cadence.

Regression safety requires coverage of default and configured window sizes, full-window startup gating, sliding eviction order, average values above, below, and equal to the threshold, persistent enabled state while the average remains at or above threshold, recovery after an unavailable read, invalid configuration rejection, and transition logs containing the decision average.

## Validation Plan

- Unit-test configuration parsing for the explicit value, the default value of `5`, and every invalid value category.
- Unit-test that no threshold-based enablement occurs before the configured number of valid readings.
- Unit-test sliding-window decisions across sequences that cross the threshold in both directions.
- Unit-test equality at the threshold.
- Unit-test that the fan remains enabled across consecutive averages at or above the threshold.
- Unit-test that an unavailable read forces the fan off, is excluded from the window, retains earlier valid samples, and allows averaging to resume on recovery.
- Unit-test transition logging against the unrounded decision average and configured threshold.
- Run the complete project test suite and formatting/static checks provided by the repository tooling.
- Run `git diff --check`.

## Documentation Needs

- Add `temperature_average_read_count: 5` to the default resource configuration.
- Add the key and its default to the README configuration example and description.
- Explain that one measurement is collected per `check_interval`, a complete window is required before initial fan enablement, and valid transition logs report the decision average.
