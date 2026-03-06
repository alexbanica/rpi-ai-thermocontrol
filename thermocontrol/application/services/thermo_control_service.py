"""Application service orchestrating temperature checks and fan toggling."""

import logging
import time
from typing import Optional

from thermocontrol.domain.entities.context_entity import ContextEntity
from thermocontrol.domain.services.rpi_service_interface import RpiServiceInterface
from thermocontrol.domain.services.temperature_service_interface import TemperatureServiceInterface
from thermocontrol.shared.constants import LogMessages


class ThermoControlService:
    def __init__(
        self,
        context: ContextEntity,
        temperature_service: TemperatureServiceInterface,
        rpi_service: RpiServiceInterface,
    ):
        self.context = context
        self.temperature_service = temperature_service
        self.rpi_service = rpi_service
        self.thermo_control_thread_is_running = True
        self.is_fan_enabled = False
        logging.info(LogMessages.INITIALIZING_THERMO_SERVICE, self.context)

    def run(self) -> None:
        while self.thermo_control_thread_is_running:
            try:
                time.sleep(self.context.thermo_check_interval)
                self.control_ai_module_fan_once()
            except KeyboardInterrupt:
                self.close()
            except Exception as error:
                logging.error(LogMessages.LOOP_ERROR, error)

    def control_ai_module_fan_once(self) -> None:
        temperature = self.temperature_service.get_temperature_ai_module()
        should_enable_fan = self._should_enable_fan(temperature)
        self.rpi_service.toggle_ai_cooler(should_enable_fan)
        self._log_fan_toggle(temperature, should_enable_fan)
        self.is_fan_enabled = should_enable_fan

    def _should_enable_fan(self, temperature: Optional[float]) -> bool:
        if temperature is None:
            return False

        return temperature >= self.context.ai_temperature_threshold

    def _log_fan_toggle(self, temperature: Optional[float], should_enable_fan: bool) -> None:
        if self.is_fan_enabled == should_enable_fan or temperature is None:
            return

        if should_enable_fan:
            logging.info(LogMessages.FAN_ENABLED_AT_TEMP, temperature, self.context.ai_temperature_threshold)
            return

        logging.info(LogMessages.FAN_DISABLED_AT_TEMP, temperature, self.context.ai_temperature_threshold)

    def close(self) -> None:
        self.thermo_control_thread_is_running = False
        self.rpi_service.close()
        logging.info(LogMessages.STOPPING)
