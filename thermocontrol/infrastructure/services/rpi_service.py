"""Infrastructure service controlling GPIO fan output."""

import logging
import time

from gpiozero import OutputDevice

from thermocontrol.domain.entities.context_entity import ContextEntity
from thermocontrol.domain.services.rpi_service_interface import RpiServiceInterface
from thermocontrol.shared.constants import LogMessages


class RpiService(RpiServiceInterface):
    def __init__(self, context: ContextEntity):
        self.context = context
        self.ai_module_fan = OutputDevice(context.ai_thermo_control_gpio_pin)

    def toggle_ai_cooler(self, enable: bool) -> None:
        self.ai_module_fan.on() if enable else self.ai_module_fan.off()

    def close(self) -> None:
        logging.info(LogMessages.CLOSING_RPI)
        if self.ai_module_fan.is_active:
            logging.info(LogMessages.TURNING_OFF_FAN)
            self.ai_module_fan.off()
            time.sleep(5)
        del self.ai_module_fan
        logging.info(LogMessages.FAN_STOPPED)
