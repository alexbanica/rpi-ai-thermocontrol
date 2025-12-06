#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

import yaml
import os

from dto import Context

class YamlHelper:
    def __init__(self, config_base_dir: str):
        self.config_dir = config_base_dir

    def parse_config(self, context: Context, config_file_names: list[str]) -> None:
        for config_file in config_file_names:
            config = None
            file_path = os.path.join(self.config_dir, config_file)
            if not os.path.exists(file_path):
                continue

            logging.info(f"Parsing config file: {file_path}")
            with open(file_path, 'r') as file:
                config = yaml.safe_load(file)

            if config is None:
                continue

            self.__parse_thermocontrol_ai_config(config, context)

    def __parse_thermocontrol_ai_config(self, config: dict, context: Context) -> None:
        thermocontrol_config = config.get('thermocontrol', {}).get('ai_module', {})
        context.ai_temperature_threshold = thermocontrol_config.get('temperature_threshold', 20)
        context.ai_thermo_control_interval = thermocontrol_config.get('thermo_control_interval', 5)
        context.ai_thermo_control_gpio_pin = thermocontrol_config.get('thermo_control_gpio_pin', 18)
