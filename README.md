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
    thermo_control_gpio_pin: 18
    thermo_control_hwmon: hwmon1,hwmon2
```

## Usage
Run the service:
```bash
python -m thermocontrol
```

Run in detached screen session:
```bash
./run.sh
```
