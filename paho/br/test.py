#! /usr/bin/env python
# -*- coding: utf-8 -*-

# test.py

from get_config import *

test = GetConfig()
broker = test.get_broker()
print "get broker"
print broker