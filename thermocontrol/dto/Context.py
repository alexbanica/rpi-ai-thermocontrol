#!/usr/bin/python
# -*- coding:utf-8 -*-

from dataclasses import dataclass

@dataclass
class Context:
    ai_temperature_threshold: int
    ai_thermo_control_interval: int
    ai_thermo_control_gpio_pin: int

    def __init__(self):
        self.ai_temperature_threshold = 20
        self.ai_thermo_control_interval = 5
        self.ai_thermo_control_gpio_pin = 18
    

    def __str__(self):
        return (f"Context(temperature_threshold={self.ai_temperature_threshold}, " +
                f"ai_module_thermo_control_interval={self.ai_thermo_control_interval})")
