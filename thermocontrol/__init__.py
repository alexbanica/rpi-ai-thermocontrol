#!/usr/bin/python
# -*- coding:utf-8 -*-

__version__ = "1.0.0"
__author__ = "Ionut-Alexandru Banica"

import os, sys
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'resources')


CONFIG_FILE_PATHS = ["config.yaml", "config.yml", "config.local.yaml", "config.local.yml"]