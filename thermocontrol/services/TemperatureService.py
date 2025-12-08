#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
from thermocontrol.dto import Context

class TemperatureService:
    def __init__(self, context: Context):
        self.context = context

    def get_temperature_ai_module(self) -> float:
        temp = 0
        hwmon_paths = self.context.ai_thermo_control_hwmon.split(",")

        for hwmon_path in hwmon_paths:
            try:
                with open(f"/sys/class/hwmon/{hwmon_path.strip()}/temp1_input", "r") as f:
                    temp = int(f.read().strip())
                    return temp / 1000.0
            except Exception as e:
                logging.warning("Failed to read temperature from %s: %s", hwmon_path.strip(), e)

        logging.error("Error occurred during reading AI module temperature. All options failed.")
        return 0