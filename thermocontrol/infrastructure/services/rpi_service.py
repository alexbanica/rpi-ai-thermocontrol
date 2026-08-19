"""Infrastructure service controlling GPIO fan output."""

import logging
import shutil
import subprocess

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
        ai_module_fan = getattr(self, "ai_module_fan", None)
        if ai_module_fan is None:
            return

        if ai_module_fan.is_active:
            logging.info(LogMessages.TURNING_OFF_FAN)
        ai_module_fan.off()

        pin_factory = ai_module_fan.pin_factory
        ai_module_fan.close()
        pin_factory.close()
        self.ai_module_fan = None

        self._persist_fan_off_state()
        logging.info(LogMessages.FAN_STOPPED)

    def _persist_fan_off_state(self) -> None:
        pinctrl = shutil.which("pinctrl")
        if pinctrl is None:
            logging.error(LogMessages.PINCTRL_NOT_FOUND)
            return

        gpio_pin = self.context.ai_thermo_control_gpio_pin
        try:
            subprocess.run(
                [pinctrl, str(gpio_pin), "op", "dl"],
                check=True,
                capture_output=True,
                text=True,
            )
        except (OSError, subprocess.CalledProcessError) as error:
            logging.error(LogMessages.FAN_OFF_PERSIST_FAILED, gpio_pin, error)
            return

        logging.info(LogMessages.FAN_OFF_PERSISTED, gpio_pin)
