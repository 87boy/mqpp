#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    main program of the subscriber
    @author: Bin Zhang
    @email: sjtuzb@gmail.com
"""

import paho.mqtt.client as mqtt

from get_config import *
from sub_lib import *

def main():
    config = GetConfig()
    broker = config.get_broker()
    broker_url = broker["url"]
    broker_port = broker["port"]
    broker_username = broker["username"]
    broker_password = broker["password"]

    client = mqtt.Client()
    client.username_pw_set(broker_username, broker_password)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_url, broker_port, 60)

    print "Awaiting..."

    client.loop_forever()

if __name__ == '__main__':
    main()

