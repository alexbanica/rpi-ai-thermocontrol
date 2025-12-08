#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
from thermocontrol.dto import Context
from gpiozero import OutputDevice


class RpiService:
    def __init__(self, context: Context):
        self.context = context
        self.ai_module_fan = OutputDevice(context.ai_thermo_control_gpio_pin)

    def toggle_ai_cooler(self, enable: bool):
        self.ai_module_fan.on() if enable else self.ai_module_fan.off()

    def __close__(self) -> None:
        logging.info("Closing RpiService")
        self.ai_module_fan.off()
        self.ai_module_fan.close()
