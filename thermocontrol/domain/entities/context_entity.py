"""Domain context entity for thermocontrol runtime configuration."""

from dataclasses import dataclass

from thermocontrol.shared.constants import Defaults


@dataclass
class ContextEntity:
    thermo_check_interval: int = Defaults.THERMO_CHECK_INTERVAL
    ai_temperature_threshold: int = Defaults.AI_TEMPERATURE_THRESHOLD
    ai_thermo_control_gpio_pin: int = Defaults.AI_THERMO_CONTROL_GPIO_PIN
    ai_thermo_control_hwmon: str = Defaults.AI_THERMO_CONTROL_HWMON
