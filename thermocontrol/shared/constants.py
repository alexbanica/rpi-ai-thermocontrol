"""Centralized constants for configuration keys and log messages."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigKeys:
    THERMOCONTROL: str = "thermocontrol"
    CHECK_INTERVAL: str = "check_interval"
    AI_MODULE: str = "ai_module"
    TEMPERATURE_THRESHOLD: str = "temperature_threshold"
    THERMO_CONTROL_GPIO_PIN: str = "thermo_control_gpio_pin"
    THERMO_CONTROL_HWMON: str = "thermo_control_hwmon"


@dataclass(frozen=True)
class Defaults:
    THERMO_CHECK_INTERVAL: int = 5
    AI_TEMPERATURE_THRESHOLD: int = 20
    AI_THERMO_CONTROL_GPIO_PIN: int = 18
    AI_THERMO_CONTROL_HWMON: str = "hwmon1"
    LOG_FILE_PATH: str = "/var/log/rpi-ai-thermocontrol.log"


@dataclass(frozen=True)
class RuntimeConfig:
    CONFIG_FILE_PATHS: tuple[str, ...] = (
        "config.yaml",
        "config.yml",
        "config.local.yaml",
        "config.local.yml",
    )


@dataclass(frozen=True)
class LogMessages:
    STARTING: str = "Starting RPI AI Thermocontrol. Press Ctrl+C to exit."
    STOPPING: str = "Stopping RPI AI Thermocontrol"
    PARSING_CONFIG_FILE: str = "Parsing config file: %s"
    PARSING_CONFIG_COMPLETE: str = "Parsing config file complete: %s"
    INITIALIZING_THERMO_SERVICE: str = "Initializing ThermoControlService with context: %s"
    TEMP_READ_FAILED: str = "Failed to read temperature from %s: %s"
    TEMP_READ_ALL_FAILED: str = "Unable to read AI module temperature from any configured hwmon device."
    LOOP_ERROR: str = "Error occurred during AI module temperature control: %s"
    FAN_ENABLED_AT_TEMP: str = "Fan enabled at temperature=%sC"
    FAN_DISABLED_AT_TEMP: str = "Fan disabled at temperature=%sC"
    CLOSING_RPI: str = "Closing RpiService"
    TURNING_OFF_FAN: str = "Turning off AI module fan"
    FAN_STOPPED: str = "Stopped AI module fan"
