# RPI AI Thermocontrol

A Raspberry Pi-based temperature control system designed to monitor and manage AI module temperature using automated fan
control.

## Features

- Real-time AI module temperature monitoring
- Automated fan control based on temperature threshold
- Configurable temperature threshold and monitoring interval
- Daemon thread for continuous temperature management
- Error handling and logging

## Setup

1. Ensure you have Python 3.12 installed on your Raspberry Pi
2. Connect a fan to the specified GPIO pin
3. Configure the temperature sensor (hwmon1)

## Configuration

The system can be configured using the following parameters:

- `ai_temperature_threshold`: Temperature threshold for fan activation (in °C)
- `ai_thermo_control_interval`: Monitoring interval in seconds
- `ai_thermo_control_gpio_pin`: GPIO pin number for fan control

## Usage

The system automatically:

- Monitors AI module temperature through the system's temperature sensor
- Activates the cooling fan when temperature exceeds the configured threshold
- Deactivates the fan when temperature drops below threshold
- Handles errors and provides logging

## Author

Ionut-Alexandru Banica

Version: 1.0.0