"""Application service orchestrating temperature checks and fan toggling."""

from collections import deque
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
        self.temperature_window: deque[float] = deque(
            maxlen=self.context.ai_temperature_average_read_count
        )
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
        should_enable_fan, decision_average = self._determine_fan_state(temperature)
        self.rpi_service.toggle_ai_cooler(should_enable_fan)
        self._log_fan_toggle(decision_average, should_enable_fan)
        self.is_fan_enabled = should_enable_fan

    def _determine_fan_state(
        self, temperature: Optional[float]
    ) -> tuple[bool, Optional[float]]:
        if temperature is None:
            return False, None

        self.temperature_window.append(temperature)
        if len(self.temperature_window) < self.context.ai_temperature_average_read_count:
            return False, None

        decision_average = sum(self.temperature_window) / len(self.temperature_window)
        return decision_average >= self.context.ai_temperature_threshold, decision_average

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
