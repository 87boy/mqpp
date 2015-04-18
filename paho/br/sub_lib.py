#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Paho Subscriber Library
    @author: Bin Zhang
    @email: sjtuzb@gmail.com
"""

import datetime
import json
import urllib
import urllib2

from get_config import *

class SubLib(object):
    """docstring for SubLib"""
    def __init__(self):
        super(SubLib, self).__init__()
        config = GetConfig()
        self.influxdb = config.get_influxdb()
        self.topics = config.get_topics()

# Called when the broker responds to our connection request.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    config = GetConfig()
    topics = config.get_topics()
    topic_list = []
    for key in topics.keys():
        topic_list.append((str(topics[key]["topic"]), topics[key]["qos"]))
    client.subscribe(topic_list)

# Called when a message has been received on a topic that the client subscribes to
def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))

    begin_datetime = str(datetime.datetime.now().isoformat())
    print "[begin] " + begin_datetime

    message = json.loads(msg.payload)

    config = GetConfig()
    influxdb = config.get_influxdb()
    influxdb_url = urllib.quote(influxdb["url"])
    influxdb_port = urllib.quote(str(influxdb["port"]))
    influxdb_database = urllib.quote(influxdb["databases"]["database"])
    influxdb_username = urllib.quote(influxdb["databases"]["username"])
    influxdb_password = urllib.quote(influxdb["databases"]["password"])

    request_url = "http://%s:%s/db/%s/series?u=%s&p=%s" % (influxdb_url, influxdb_port, influxdb_database, influxdb_username, influxdb_password)

    for record in message:
        if not record["device"]:
            continue

        post_dict = {}
        post_dict["name"] = record["device"]
        del record["device"]

        column_list = []
        point = []
        point_list = []

        if "timestamp" in record:
            column_list.append("time")
            point.append(record["timestamp"])
            del record["timestamp"]
        if "id" in record:
            column_list.append("sequence_number")
            point.append(record["id"])
            del record["id"]
        for key in record.keys():
            column_list.append(key)
            point.append(record[key])

        point_list.append(point)
        post_dict["columns"] = column_list
        post_dict["points"] = point_list
        post_list = [post_dict]

        post_str = json.dumps(post_list)

        try:
            request = urllib2.Request(request_url, post_str)
            request.add_header("Content-Type", "application/json")
            response = urllib2.urlopen(request, timeout=10)
        except:
            print "HTTPError!"

        print response.code

