#!/usr/bin/python
# -*- coding:utf-8 -*-

from thermocontrol.dto import Context

class TemperatureService:
    def __init__(self, context: Context):
        self.context = context

    def get_temperature_ai_module(self) -> float:
        with open(f"/sys/class/hwmon/{self.context.ai_thermo_control_hwmon}/temp1_input", "r") as f:
            temp = int(f.read().strip())
        return temp / 1000.0
