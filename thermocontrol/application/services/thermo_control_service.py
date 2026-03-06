"""Application service orchestrating temperature checks and fan toggling."""

import logging
import time

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
        self.rpi_service.toggle_ai_cooler(temperature >= self.context.ai_temperature_threshold)

    def close(self) -> None:
        self.thermo_control_thread_is_running = False
        self.rpi_service.close()
        logging.info(LogMessages.STOPPING)
