#!/usr/bin/python
# -*- coding:utf-8 -*-

from dataclasses import dataclass

@dataclass
class Context:
    temperature_threshold: int

    def __str__(self):
        return (f"Context(temperature_threshold={self.temperature_threshold}, " +
               ")")
