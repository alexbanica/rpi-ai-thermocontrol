"""Presentation controller wiring dependencies and running thermocontrol."""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

from thermocontrol.application.services.thermo_control_service import ThermoControlService
from thermocontrol.domain.entities.context_entity import ContextEntity
from thermocontrol.infrastructure.parsers.yaml_config_parser import YamlConfigParser
from thermocontrol.infrastructure.services.rpi_service import RpiService
from thermocontrol.infrastructure.services.temperature_service import TemperatureService
from thermocontrol.shared.constants import Defaults, LogMessages, RuntimeConfig


class RuntimeController:
    def __init__(self):
        self.resources_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))),
            "resources",
        )

    def run(self) -> int:
        context = ContextEntity()
        try:
            self._setup_logging()
            logging.info(LogMessages.STARTING)
            config_parser = YamlConfigParser(self.resources_dir)
            config_parser.parse_config(context, list(RuntimeConfig.CONFIG_FILE_PATHS))
            service = ThermoControlService(
                context=context,
                temperature_service=TemperatureService(context),
                rpi_service=RpiService(context),
            )
            service.run()
            return 0
        except Exception as error:
            logging.error("Error starting RPI AI Thermocontrol: %s", error)
            return 1

    @staticmethod
    def _setup_logging() -> None:
        file_handler = TimedRotatingFileHandler(
            Defaults.LOG_FILE_PATH,
            when="midnight",
            interval=1,
            backupCount=5,
        )
        console_handler = logging.StreamHandler()
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] [%(threadName)s]: %(message)s",
            handlers=[file_handler, console_handler],
        )
