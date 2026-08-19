# Persist Fan-Off State After Shutdown

Status: Approved

## Purpose

Keep the AI module fan off after a graceful application shutdown instead of
allowing GPIO cleanup to return the control pin to an undriven state that turns
the fan back on.

## Requested Behavior

- A graceful shutdown requests the fan off before releasing GPIO resources.
- After GPIO Zero and its pin factory release the configured GPIO, Raspberry
  Pi `pinctrl` configures that GPIO as an output driven low.
- A repeated close is safe and does not access an already closed device.
- Missing `pinctrl`, insufficient permission, or a failed command is logged and
  does not prevent process shutdown.

## Scope

- `RpiService` graceful shutdown behavior.
- Shutdown diagnostics for the persistent fan-off operation.

## Out Of Scope

- Maintaining the state after power loss or reboot.
- Guaranteeing the state after `SIGKILL`, a crash before graceful cleanup, or
  another process reconfiguring the GPIO.
- Electrical fail-safe behavior when `pinctrl` is unavailable.
- Automated tests for the GPIO adapter, which are prohibited by the project's
  domain-only test policy.

## Definitions

- **Graceful shutdown:** shutdown that reaches `RpiService.close()`.
- **Persistent fan-off state:** the configured GPIO remains an output driven
  low after this application releases it and exits.

## Inputs And Constraints

- The fan control GPIO comes from `ContextEntity.ai_thermo_control_gpio_pin`.
- The host must provide Raspberry Pi's `pinctrl` utility and permission to use
  it. Current Raspberry Pi operation runs the application with elevated
  permission.
- The fan wiring must interpret a low control signal as off.

## Deterministic Behavior Delivered

1. Drive the fan output low on every first close call.
2. Explicitly close the GPIO Zero output device and its pin factory.
3. Run `pinctrl <gpio> op dl` without a shell so the released pin is restored as
   an output driven low.
4. Log success or an actionable failure and finish shutdown.
5. Ignore later close calls after the device reference has been cleared.

## Assumptions

- `RpiService` is the only GPIO Zero consumer in this process when application
  shutdown begins, so closing its shared pin factory is safe.
- The reported behavior occurs on the Raspberry Pi `lgpio` deployment described
  by the repository documentation.

## Impact

- Normal application shutdown no longer leaves the fan control input floating.
- The previous five-second shutdown delay is removed because waiting while the
  output is low does not affect its state after GPIO release.
- A hardware pull-down resistor remains the recommended electrical fail-safe.

## Validation Performed

- Python compilation of the changed modules.
- Git whitespace validation.

## Validation Skipped

- Live Raspberry Pi GPIO and fan observation; unavailable in this workspace.
- Ruff static checking; Ruff is not installed in this checkout.
- Automated adapter tests; prohibited by the domain-only test policy.
- QA and code review; skipped by the `super-agent` workflow.

## Documentation Changes

- This completed-work specification records the runtime and hardware boundary.
