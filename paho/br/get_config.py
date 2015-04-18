#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Get config
    @author: Bin Zhang
    @email: sjtuzb@gmail.com
"""

import os
import datetime
import json

class GetConfig(object):
    """docstring for GetConfig"""
    def __init__(self):
        super(GetConfig, self).__init__()
        cwd = os.getcwd()
        config_path = cwd + "/config.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as config_file:
                config_string = config_file.read()
                self.config_json = json.loads(config_string)
        else:
            log_path = cwd + "/config.log"
            with open(log_path, "a") as log_file:
                log_json = {"datatime": str(datetime.datetime.now().isoformat()), "error": "config file does not exist!"}
                json.dump(log_json, log_file)

    def get_broker(self):
        return self.config_json["broker"]
    def get_ckan(self):
        return self.config_json["ckan"]
    def get_influxdb(self):
        return self.config_json["influxdb"]
    def get_topics(self):
        return self.config_json["topics"]

