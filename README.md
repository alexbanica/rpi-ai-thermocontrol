# RPI AI Thermocontrol

Python-based temperature control for AI module cooling with GPIO fan management.

## Architecture
The codebase uses a DDD/onion layout:
- `thermocontrol/domain`: entities and interfaces
- `thermocontrol/application`: use-case orchestration services
- `thermocontrol/infrastructure`: GPIO and YAML adapters
- `thermocontrol/presentation`: runtime controller and entrypoint
- `thermocontrol/shared`: centralized constants

## Installation
1. Create virtualenv:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install base dependencies:
```bash
pip install -r requirements.txt
```

3. Install platform-specific extras:
- Raspberry Pi:
```bash
pip install -r requirements/rpi.txt
```
- Jetson:
```bash
pip install -r requirements/jetson.txt
```
- Sunrise X3:
```bash
pip install -r requirements/sunrise_x3.txt
```

4. Install package:
```bash
pip install .
```

5. Install developer dependencies (optional):
```bash
pip install -r requirements.dev.txt
```

## Configuration
Default config path: `resources/config.yml`

Example:
```yaml
thermocontrol:
  check_interval: 10
  ai_module:
    temperature_threshold: 55
    temperature_average_read_count: 5
    thermo_control_gpio_pin: 18
    thermo_control_hwmon: hwmon1,hwmon2
```

`temperature_average_read_count` controls the number of recent valid AI-module
temperature measurements used for fan decisions. It defaults to `5` when
omitted and must be an integer greater than or equal to `1`.

One measurement is attempted per `check_interval`. The fan stays off until a
complete averaging window has been collected, so the default configuration
requires five valid measurement cycles before the first threshold decision. If
a read fails, the fan is immediately requested off, the failed read is excluded,
and previously collected valid measurements remain available when reading
recovers.

## Usage
Run the service:
```bash
python -m thermocontrol
```

Run in detached screen session:
```bash
./run.sh
```

## Logging Behavior
- Fan state transition logs are emitted only when state changes:
  - `Fan enabled at temperature=<current_celsius>/<threshold_celsius>C`
  - `Fan disabled at temperature=<current_celsius>/<threshold_celsius>C`
- For valid temperature-driven transitions, `current_celsius` is the unrounded
  decision average from the full measurement window.
- If no configured hwmon device can be read, the service logs warnings and keeps the fan off.

## Release Workflow

This repository uses a released workflow that requires:

- A stable `MAJOR.MINOR.PATCH` tag or beta `MAJOR.MINOR.PATCH-betaN` tag, where
  `N` is a positive integer
- Stable tags map to the same package version; beta tags map to PEP 440
  `MAJOR.MINOR.PATCHbN`
- The tag commit to be on `main`
- The package to be published to Forgejo public organization storage at
  `https://forgejo.alexlab.nl/api/packages/public/pypi`

Required GitHub Actions secrets:

- `FORGEJO_PACKAGE_USERNAME`
- `FORGEJO_PACKAGE_TOKEN`

`.github/workflows/ci.yml` runs lint and tests on pull requests targeting `main`
and pushes to `main`, using check names `Lint` and `Tests`.
`.github/workflows/publish.yml` repeats those gates for supported stable and beta
tags, then publishes in `Publish Forgejo package` after both pass. Both workflows
pin external actions to immutable commit SHAs, disable persisted checkout
credentials, and use per-workflow/per-ref concurrency. Dependabot groups weekly
GitHub Actions updates.

Public install check (anonymous):

```bash
pip install --index-url https://forgejo.alexlab.nl/api/packages/public/pypi/simple rpi-ai-thermocontrol==<exact version>
```

Publishing behavior:

- Matching versions cannot be overwritten; a duplicate published version fails.
- The first release is delivered as DRAFT until a live push of a matching tag
  confirms the anonymous download of that exact version works in Forgejo.

Operator-owned setup requirements:

- Configure branch protection or rulesets so `Lint` and `Tests` must pass before
  merging to `main`.
- Restrict release-tag creation to trusted maintainers.
- Set the two Forgejo secrets above in repository settings.
