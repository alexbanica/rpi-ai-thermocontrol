"""Infrastructure parser for YAML runtime configuration."""

import logging
import os

import yaml

from thermocontrol.domain.entities.context_entity import ContextEntity
from thermocontrol.domain.services.config_parser_interface import ConfigParserInterface
from thermocontrol.shared.constants import ConfigKeys, Defaults, LogMessages


class YamlConfigParser(ConfigParserInterface):
    def __init__(self, config_base_dir: str):
        self.config_dir = config_base_dir

    def parse_config(self, context: ContextEntity, config_file_names: list[str]) -> None:
        for config_file_name in config_file_names:
            file_path = os.path.join(self.config_dir, config_file_name)
            if not os.path.exists(file_path):
                continue

            logging.info(LogMessages.PARSING_CONFIG_FILE, file_path)
            with open(file_path, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)

            if config is None:
                continue

            self._parse_thermocontrol_config(config, context)
            self._parse_thermocontrol_ai_config(config, context)
            logging.info(LogMessages.PARSING_CONFIG_COMPLETE, file_path)

    def _parse_thermocontrol_config(self, config: dict, context: ContextEntity) -> None:
        thermocontrol_config = config.get(ConfigKeys.THERMOCONTROL, {})
        context.thermo_check_interval = thermocontrol_config.get(
            ConfigKeys.CHECK_INTERVAL, Defaults.THERMO_CHECK_INTERVAL
        )

    def _parse_thermocontrol_ai_config(self, config: dict, context: ContextEntity) -> None:
        ai_module_config = config.get(ConfigKeys.THERMOCONTROL, {}).get(ConfigKeys.AI_MODULE, {})
        context.ai_temperature_threshold = ai_module_config.get(
            ConfigKeys.TEMPERATURE_THRESHOLD, Defaults.AI_TEMPERATURE_THRESHOLD
        )
        context.ai_thermo_control_gpio_pin = ai_module_config.get(
            ConfigKeys.THERMO_CONTROL_GPIO_PIN, Defaults.AI_THERMO_CONTROL_GPIO_PIN
        )
        context.ai_thermo_control_hwmon = ai_module_config.get(
            ConfigKeys.THERMO_CONTROL_HWMON, Defaults.AI_THERMO_CONTROL_HWMON
        )
