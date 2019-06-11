#!/usr/local/bin/python3
#coding=utf-8

import sys
print(sys.path)

from common_utils.time_function import format_to_ymdx, time_calculate, format_to_ymd

print(format_to_ymdx())
print(time_calculate(1))
print(format_to_ymd())


