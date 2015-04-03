#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Message Queue Receiver
    @author: Bin Zhang
    @email: sjtuzb@gmail.com
'''

import datetime
import json
import urllib
import urllib2

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

    begin_datetime = str(datetime.datetime.now().isoformat())
    print '[begin] ' + begin_datetime

    message = json.loads(msg.payload)
    print message

    post_data = str(msg.payload)

    global influxdb_url
    global influxdb_port
    global influxdb_dbname
    global influxdb_username
    global influxdb_password

    influxdb_url = urllib.quote(influxdb_url)
    influxdb_port = urllib.quote(str(influxdb_port))
    influxdb_dbname = urllib.quote(influxdb_dbname)
    influxdb_username = urllib.quote(influxdb_username)
    influxdb_password = urllib.quote(influxdb_password)

    request_url = "http://%s:%s/db/%s/series?u=%s&p=%s" % (influxdb_url, influxdb_port, influxdb_dbname, influxdb_username, influxdb_password)
    print request_url
    request = urllib2.Request(request_url, post_data)
    request.add_header("Content-Type", "application/json")
    response = urllib2.urlopen(request, timeout=10)
    #assert response.code == 200
    print response.code
    #response_dict = json.loads(response.read())
    #print response_dict

client = mqtt.Client()
client.username_pw_set(broker_username, broker_password)

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_url, broker_port, 60)

print 'Awaiting...'

client.loop_forever()

