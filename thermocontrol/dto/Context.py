#!/usr/bin/python
# -*- coding:utf-8 -*-

from dataclasses import dataclass

@dataclass
class Context:
    thermo_check_interval: int
    ai_temperature_threshold: int
    ai_thermo_control_gpio_pin: int
    ai_thermo_control_hwmon: str

    def __init__(self):
        self.ai_temperature_threshold = 20
        self.thermo_check_interval = 5
        self.ai_thermo_control_gpio_pin = 18
        self.ai_thermo_control_hwmon = "hwmon1"
    

    def __str__(self):
        return (f"Context(temperature_threshold={self.ai_temperature_threshold}, " +
                f"thermo_check_interval={self.thermo_check_interval}, " +
                f"gpio_pin={self.ai_thermo_control_gpio_pin}, " +
                f"hwmon={self.ai_thermo_control_hwmon})")
