# -*- coding: utf-8 -*-

import math


LOG_BASE = 10.0


def scale_to_log(value: float, base: float = LOG_BASE):
    return math.log(value, base)


def scale_from_log(value: float, base: float = LOG_BASE):
    return base ** value
