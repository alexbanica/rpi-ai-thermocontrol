"""Infrastructure service reading temperatures from sysfs hwmon files."""

import logging
from typing import Optional

from thermocontrol.domain.entities.context_entity import ContextEntity
from thermocontrol.domain.services.temperature_service_interface import TemperatureServiceInterface
from thermocontrol.shared.constants import LogMessages


class TemperatureService(TemperatureServiceInterface):
    def __init__(self, context: ContextEntity):
        self.context = context

    def get_temperature_ai_module(self) -> Optional[float]:
        hwmon_paths = self.context.ai_thermo_control_hwmon.split(",")

        for hwmon_path in hwmon_paths:
            trimmed_path = hwmon_path.strip()
            try:
                with open(f"/sys/class/hwmon/{trimmed_path}/temp1_input", "r", encoding="utf-8") as file:
                    return int(file.read().strip()) / 1000.0
            except Exception as error:
                logging.warning(LogMessages.TEMP_READ_FAILED, trimmed_path, error)

        logging.warning(LogMessages.TEMP_READ_ALL_FAILED)
        return None
