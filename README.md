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
2. Connect a fan to the specified GPIO pin (default: GPIO18)
3. Configure the temperature sensor path in /sys/class/hwmon/
4. Verify the hwmon device number (default: hwmon1)

## Installation

1. Clone this repository
2. Install required dependencies using pip:

## Configuration

The system can be configured by modifying the following parameters:

- `ai_temperature_threshold`: Temperature threshold for fan activation in °C (default: 20)
- `thermo_check_interval`: Monitoring interval in seconds (default: 5)
- `ai_thermo_control_gpio_pin`: GPIO pin number for fan control (default: 18)
- `ai_thermo_control_hwmon`: Hardware monitor device name (default: "hwmon1")

Configuration can be done through YAML configuration file or by modifying the Context class defaults.

## Usage

The system automatically:

- Monitors AI module temperature through the specified hwmon device
- Checks temperature at configured intervals (default: 5 seconds)
- Activates the cooling fan when temperature exceeds the threshold (default: 20°C)
- Deactivates the fan when temperature drops below threshold
- Handles errors and provides logging
- Runs as a daemon thread for continuous operation

## Author

Ionut-Alexandru Banica

Version: 1.0.0