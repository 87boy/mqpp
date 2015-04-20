#! /usr/bin/env python
# -*- coding: utf-8 -*-

# test.py

import random

from gateway_lib import *

#test_data = [{"device": "test", "timestamp": 1428928106333, "id": 5, "minimum": 1, "average": 2, "maximum": 3}, {"device": "test", "timestamp": 1428928106366, "id": 4, "minimum": 2, "average": 4, "maximum": 6}]

#test_data = {"device": "test", "timestamp": 1428928106333, "id": 6, "minimum": 1, "average": 2, "maximum": 3}

#test_data = [[1,2,3]]

test_data = [{"device":"test", "data":[1,2,3]}]

gateway_config()

gateway_puber(test_data)
