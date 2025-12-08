#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import time
from time import sleep

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
        if self.ai_module_fan.is_active:
            logging.info("Turning off AI module fan")
            self.ai_module_fan.off()
            time.sleep(5)
        del self.ai_module_fan
        logging.info("Stopped AI module fan")