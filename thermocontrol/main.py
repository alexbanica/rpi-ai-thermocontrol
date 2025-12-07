#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import os

from logging.handlers import TimedRotatingFileHandler
from thermocontrol.helpers import YamlHelper
from thermocontrol.dto import Context
from thermocontrol.services.ThermoControlService import ThermoControlService

RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'resources')
CONFIG_FILE_PATHS = ["config.yaml", "config.yml", "config.local.yaml", "config.local.yml"]

def _setup_logging():
    file_handler = TimedRotatingFileHandler(
        '/var/log/rpi-ai-thermocontrol.log',
        when='midnight',
        interval=1,
        backupCount=5
    )
    console_handler = logging.StreamHandler()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(threadName)s]: %(message)s",
        handlers=[file_handler, console_handler]
    )

def main(context: Context):
    try:
        _setup_logging()
        logging.info("Starting RPI AI Thermocontrol. Press Ctrl+C to exit.")
        YamlHelper(RESOURCES_DIR).parse_config(context, CONFIG_FILE_PATHS)
        ThermoControlService(context)

    except Exception as e:
        logging.error("Error starting RPI AI Thermocontrol: %s", e)
        exit(1)