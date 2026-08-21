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

    def parse_selected_config(self, context: ContextEntity, file_path: str) -> None:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Selected configuration is not a regular file: {file_path}")

        logging.info(LogMessages.PARSING_CONFIG_FILE, file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        if config is None:
            return
        if not isinstance(config, dict):
            raise ValueError("Selected configuration root must be a mapping")

        thermocontrol_config = config.get(ConfigKeys.THERMOCONTROL)
        if thermocontrol_config is None and ConfigKeys.THERMOCONTROL not in config:
            logging.info(LogMessages.PARSING_CONFIG_COMPLETE, file_path)
            return
        if not isinstance(thermocontrol_config, dict):
            raise ValueError(f"{ConfigKeys.THERMOCONTROL} must be a mapping")

        updates = {}
        if ConfigKeys.CHECK_INTERVAL in thermocontrol_config:
            updates["thermo_check_interval"] = thermocontrol_config[
                ConfigKeys.CHECK_INTERVAL
            ]

        ai_module_config = thermocontrol_config.get(ConfigKeys.AI_MODULE)
        if ai_module_config is None and ConfigKeys.AI_MODULE not in thermocontrol_config:
            ai_module_config = {}
        if not isinstance(ai_module_config, dict):
            raise ValueError(f"{ConfigKeys.AI_MODULE} must be a mapping")

        if ConfigKeys.TEMPERATURE_THRESHOLD in ai_module_config:
            updates["ai_temperature_threshold"] = ai_module_config[
                ConfigKeys.TEMPERATURE_THRESHOLD
            ]
        if ConfigKeys.TEMPERATURE_AVERAGE_READ_COUNT in ai_module_config:
            average_read_count = ai_module_config[
                ConfigKeys.TEMPERATURE_AVERAGE_READ_COUNT
            ]
            if type(average_read_count) is not int or average_read_count < 1:
                raise ValueError(
                    f"{ConfigKeys.TEMPERATURE_AVERAGE_READ_COUNT} must be an integer "
                    "greater than or equal to 1"
                )
            updates["ai_temperature_average_read_count"] = average_read_count
        if ConfigKeys.THERMO_CONTROL_GPIO_PIN in ai_module_config:
            updates["ai_thermo_control_gpio_pin"] = ai_module_config[
                ConfigKeys.THERMO_CONTROL_GPIO_PIN
            ]
        if ConfigKeys.THERMO_CONTROL_HWMON in ai_module_config:
            updates["ai_thermo_control_hwmon"] = ai_module_config[
                ConfigKeys.THERMO_CONTROL_HWMON
            ]

        for attribute, value in updates.items():
            setattr(context, attribute, value)

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
        average_read_count = ai_module_config.get(
            ConfigKeys.TEMPERATURE_AVERAGE_READ_COUNT,
            Defaults.AI_TEMPERATURE_AVERAGE_READ_COUNT,
        )
        if type(average_read_count) is not int or average_read_count < 1:
            raise ValueError(
                f"{ConfigKeys.TEMPERATURE_AVERAGE_READ_COUNT} must be an integer "
                "greater than or equal to 1"
            )
        context.ai_temperature_average_read_count = average_read_count
        context.ai_thermo_control_gpio_pin = ai_module_config.get(
            ConfigKeys.THERMO_CONTROL_GPIO_PIN, Defaults.AI_THERMO_CONTROL_GPIO_PIN
        )
        context.ai_thermo_control_hwmon = ai_module_config.get(
            ConfigKeys.THERMO_CONTROL_HWMON, Defaults.AI_THERMO_CONTROL_HWMON
        )
