#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
from thermocontrol.dto import Context

class TemperatureService:
    def __init__(self, context: Context):
        self.context = context

    def get_temperature_ai_module(self) -> float:
        return 45
