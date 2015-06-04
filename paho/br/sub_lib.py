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

# Called when a message has been received on a topic that the client
# subscribes to


def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))

    message = json.loads(msg.payload)
    if not isinstance(message, list):
        return

    config = GetConfig()
    influxdb = config.get_influxdb()
    influxdb_url = urllib.quote(influxdb["url"])
    influxdb_port = urllib.quote(str(influxdb["port"]))
    influxdb_database = urllib.quote(influxdb["databases"]["database"])
    influxdb_username = urllib.quote(influxdb["databases"]["username"])
    influxdb_password = urllib.quote(influxdb["databases"]["password"])

    request_url = "http://%s:%s/db/%s/series?u=%s&p=%s" % (
        influxdb_url, influxdb_port, influxdb_database, influxdb_username, influxdb_password)

    for record in message:
        if not isinstance(record, dict):
            continue
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

        request = urllib2.Request(request_url, post_str)
        request.add_header("Content-Type", "application/json")
        cwd = os.getcwd()
        log_path = cwd + "/error.log"
        try:
            response = urllib2.urlopen(request, timeout=10)
        except urllib2.HTTPError as error:
            error_datetime = str(datetime.datetime.now().isoformat())
            with open(log_path, "a") as log_file:
                log_json = {"datetime": error_datetime, "error": "First HTTPError", "topic": msg.topic, "payload": msg.payload, "request_url": request_url, "post_str": post_str, "error.code": error.code}
                json.dump(log_json, log_file)
                log_file.write('\n')
        except urllib2.URLError as error:
            error_datetime = str(datetime.datetime.now().isoformat())
            with open(log_path, "a") as log_file:
                log_json = {"datetime": error_datetime, "error": "First URLError", "topic": msg.topic, "request_url": request_url, "error.reason": error.reason}
                json.dump(log_json, log_file)
                log_file.write('\n')
        except:
            error_datetime = str(datetime.datetime.now().isoformat())
            with open(log_path, "a") as log_file:
                log_json = {"datetime": error_datetime, "error": "First UnknowError", "topic": msg.topic, "payload": msg.payload, "request_url": request_url, "post_str": post_str}
                json.dump(log_json, log_file)
                log_file.write('\n')

        # print response.code
