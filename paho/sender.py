#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Message Queue Sender
    @author: Bin Zhang
    @email: sjtuzb@gmail.com
'''

import datetime
import json
import random

import paho.mqtt.client as mqtt

from config import *

message = {}

# Called when the broker responds to our connection request.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.username_pw_set(broker_username, broker_password)

client.on_connect = on_connect

client.connect(broker_url, broker_port, 60)

client.loop_start()

test_data = [{"name": "log_lines","columns": ["time", "sequence_number", "line"],"points": [[1400425947398, 9, "this line is seventh"],[1400425947399, 10, "and this is eighth"]]}]

message = test_data

message_json = json.dumps(message)

client.publish("gateway", message_json)
