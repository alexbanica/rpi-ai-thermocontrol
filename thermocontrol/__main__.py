#!/usr/bin/python
# -*- coding:utf-8 -*-
from thermocontrol.dto import Context
from thermocontrol.main import main

if __name__ == "__main__":
    context = Context()

    main(context)
    exit(0)