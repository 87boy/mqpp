#! /usr/bin/env python
# -*- coding=UTF-8 -*-

"""
    Message Queue Consumer
    @author: Bin Zhang
    @email: sjtuzb@gmail.com
"""

import datetime
import json

import paho.mqtt.client as mqtt

from config import *

# Called when the broker responds to our connection request.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("gateway")

# Called when a message has been received on a topic that the client subscribes to
def on_message(client, userdata, msg):
    """callback function"""
    print(msg.topic + " " + str(msg.payload))

    rev_datetime = str(datetime.datetime.now().isoformat())
    print '[Receive] ' + rev_datetime

client = mqtt.Client()
client.username_pw_set(broker_username, broker_password)

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_url, broker_port, 60)

print 'Awaiting...'

client.loop_forever()
