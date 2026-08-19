# RPI AI Thermocontrol

Python service that reads an AI module temperature from Linux hwmon and controls
a cooling fan through a GPIO output.

## Service behavior

- The service reads the first available configured
  `/sys/class/hwmon/<name>/temp1_input` value once per `check_interval`.
- It keeps a sliding window of valid readings and enables the fan when the full
  window's average is greater than or equal to `temperature_threshold`.
- The fan remains off while the initial window is being collected.
- A failed reading is not added to the window and immediately requests the fan
  off. Earlier valid readings remain available when reading recovers.
- `Ctrl+C` performs graceful shutdown: the service drives the fan output low,
  closes GPIO Zero, and uses `pinctrl` to keep the configured GPIO driven low
  after the process exits.

The persistent fan-off step requires Raspberry Pi `pinctrl`, permission to run
it, and wiring where a low control signal means off. It is not guaranteed after
`SIGKILL`, a crash before cleanup, a reboot, or another process reconfiguring the
GPIO. A hardware pull-down remains the electrical fail-safe.

## Architecture

The codebase uses a DDD/onion layout:

- `thermocontrol/domain`: configuration state entities and service contracts
- `thermocontrol/application`: fan-control use-case orchestration
- `thermocontrol/infrastructure`: YAML, hwmon, GPIO Zero, and `pinctrl` adapters
- `thermocontrol/presentation`: runtime wiring and process coordination
- `thermocontrol/shared`: constants and shared values

Dependencies point inward: domain code does not depend on platform or runtime
adapters.

## Requirements

- Python 3.9 or newer
- Linux hwmon entries for the configured temperature devices
- A GPIO backend supported by GPIO Zero
- Permission to access GPIO, write `/var/log/rpi-ai-thermocontrol.log`, and run
  `pinctrl` during graceful shutdown

## Installation from a checkout

Create a virtual environment and install the project:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
```

Platform dependency files are also available:

```bash
# Raspberry Pi using RPi.GPIO
python -m pip install -r requirements/rpi.txt

# NVIDIA Jetson
python -m pip install -r requirements/jetson.txt

# Sunrise X3
python -m pip install -r requirements/sunrise_x3.txt
```

Install developer tooling only when needed:

```bash
python -m pip install -r requirements.dev.txt
```

### Raspberry Pi 5 with Python 3.13

Use the OS-provided `lgpio` backend:

```bash
sudo apt update
sudo apt install python3-lgpio
```

Allow the project virtual environment to see OS-provided Python packages by
setting this value in `.venv/pyvenv.cfg`:

```ini
include-system-site-packages = true
```

Verify the backend:

```bash
.venv/bin/python -c 'import lgpio; print("lgpio loaded from", lgpio.__file__)'
```

Select it at runtime with `GPIOZERO_PIN_FACTORY=lgpio`, as shown below.

## Configuration

The runtime looks for these files, in order, under the `resources/` directory
next to the source checkout's `thermocontrol/` package:

1. `config.yaml`
2. `config.yml`
3. `config.local.yaml`
4. `config.local.yml`

Every discovered file is parsed in sequence. Values in a later file replace
earlier values, while keys omitted from that later file reset to the code
defaults. The repository default is `resources/config.yml`:

```yaml
thermocontrol:
  check_interval: 10
  ai_module:
    temperature_threshold: 60
    temperature_average_read_count: 5
    thermo_control_gpio_pin: 18
    thermo_control_hwmon: hwmon1,hwmon2
```

`thermo_control_hwmon` is a comma-separated fallback list. Each temperature file
contains millidegrees Celsius and is converted to Celsius before the decision.

`temperature_average_read_count` must be an integer greater than or equal to
`1`. If configuration files or individual values are absent, the code defaults
to a 5-second interval, 20 C threshold, 5-reading window, GPIO 18, and `hwmon1`.

## Running the service

Run from the repository root so the checked-out `resources/` configuration is
used:

```bash
sudo env GPIOZERO_PIN_FACTORY=lgpio .venv/bin/python -m thermocontrol
```

For a detached screen session:

```bash
sudo screen -dmS thermocontrol \
  env GPIOZERO_PIN_FACTORY=lgpio \
  "$PWD/.venv/bin/python" -m thermocontrol
sudo screen -r thermocontrol
```

Press `Ctrl+C` in the attached session for graceful fan cleanup. The repository
does not provide a systemd unit.

## Logging

Logs are written both to stderr and `/var/log/rpi-ai-thermocontrol.log`. The log
file rotates at midnight, with five backups retained.

Fan transition messages are emitted only when state changes:

- `Fan enabled at temperature=<current_celsius>/<threshold_celsius>C`
- `Fan disabled at temperature=<current_celsius>/<threshold_celsius>C`

For temperature-driven transitions, `current_celsius` is the unrounded average
from the full measurement window. Read failures and failed persistent fan-off
operations are logged as warnings or errors.

## Development validation

```bash
ruff check .
python -m pytest
```

Repository policy permits creating or maintaining automated tests only for
deterministic domain source logic. Use static, syntax, lint, build, dry-run,
smoke, runtime, or operator checks for non-domain changes.

## Release workflow

`.github/workflows/ci.yml` runs Python 3.9 `Lint` and `Tests` jobs for pull
requests targeting `main` and pushes to `main`.

`.github/workflows/publish.yml` accepts unprefixed stable
`MAJOR.MINOR.PATCH` tags and beta `MAJOR.MINOR.PATCH-betaN` tags. Stable tags map
directly to the package version; beta tags map to the PEP 440 form
`MAJOR.MINOR.PATCHbN`. After lint and tests pass, the workflow builds one wheel
and one source distribution, checks both with Twine, publishes them to Forgejo,
and verifies anonymous installation of the exact version.

Required GitHub Actions secrets:

- `FORGEJO_PACKAGE_USERNAME`
- `FORGEJO_PACKAGE_TOKEN`

Public installation uses Forgejo for this project and public PyPI for third-party
dependencies:

```bash
python -m pip install \
  --index-url https://forgejo.alexlab.nl/api/packages/public/pypi/simple \
  --extra-index-url https://pypi.org/simple \
  rpi-ai-thermocontrol==<exact version>
```

Published versions cannot be overwritten. Repository operators must protect
release-tag creation and configure the `Lint` and `Tests` checks as required
before merging; the publish workflow itself does not verify that a tagged commit
belongs to `main`.
