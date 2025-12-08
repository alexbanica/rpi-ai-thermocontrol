#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
from thermocontrol.dto import Context

class TemperatureService:
    def __init__(self, context: Context):
        self.context = context

    def get_temperature_ai_module(self) -> float:
        temp = 0
        try: 
            with open(f"/sys/class/hwmon/{self.context.ai_thermo_control_hwmon}/temp1_input", "r") as f:
                temp = int(f.read().strip())
            return temp / 1000.0
        except Exception as e:
            logging.error("Error occurred during reading AI module temperature: %s", e)
            return 0
