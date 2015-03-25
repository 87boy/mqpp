#! /usr/bin/env python
# -*- coding=UTF-8 -*-

"""
    Message Queue Consumer
    @author: Bin Zhang
    @email: zhangbinsjtu@gmail.com
"""

import datetime
import json

import paho.mqtt.client as mqtt

import ckan_api
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
    api_key = message['api_key']
    gateway_uuid = message['gateway_uuid']
    gateway_name = message['gateway_name']
    sensor_list = message['sensor_list']

    action = 'user_list'
    data_dict = {}
    user_list = ckan_api.ckan_api(url, api_key, action, data_dict)
    user_exist_flag = False
    for user in user_list:
        if 'apikey' in user:
            # if api_key == user['apikey']:
            user_exist_flag = True
            break
    if not user_exist_flag:
        return

    action = 'datastore_search'
    data_dict = {
        'resource_id': gateways_resource_uuid
    }
    gateways_resource = ckan_api.ckan_api(url, admin_api_key, action, data_dict)
    gateway_registered_flag = False

    for gateway in gateways_resource['records']:
        if gateway_uuid == gateway['gateway_uuid']:
            gateway_registered_flag = True
            gateway_resource_uuid = gateway['gateway_resource_uuid']
            gateway_dataset_uuid = gateway['gateway_dataset_uuid']
            break

    if gateway_registered_flag:    # gateway registered, check sensors registered or not
        # print 'gateway registered'

        action = 'datastore_search'
        data_dict = {
            'resource_id': gateway_resource_uuid
        }
        sensors_resource = ckan_api.ckan_api(url, admin_api_key, action, data_dict)
        for sensor1 in sensor_list:
            sensor_registered_flag = False

            for sensor2 in sensors_resource['records']:
                if sensor1['sensor_uuid'] == sensor2['sensor_uuid']:   # sensor registered
                    sensor_registered_flag = True
                    sensor_resource_uuid = sensor2['sensor_resource_uuid']
                    break

            if sensor_registered_flag: # sensor registered, store sensor value
                action = 'datastore_upsert'
                records = [{
                    'sensor_value': sensor1['sensor_value'],
                    'sensor_unit': sensor1['sensor_unit'],
                    'datetime': sensor1['datetime'],
                    'longitude': sensor1['longitude'],
                    'latitude': sensor1['latitude']
                }]
                data_dict = {
                    'resource_id': sensor_resource_uuid,
                    'force': True,
                    'records': records,
                    'method': 'insert'
                }
                ckan_api.ckan_api(url, api_key, action, data_dict)

            else:   # sensor not registered, create [sensor_name]_resource
                sensor_uuid = sensor1['sensor_uuid']
                sensor_name = sensor1['sensor_name']
                sensor_type = sensor1['sensor_type']

                print '    sensor ' + sensor_name + ' not registered'
                print '    sensor ' + sensor_name + ' start registering'

                # 1. resource_create
                action = 'resource_create'
                data_dict = {
                    'package_id': gateway_dataset_uuid,
                    'url': 'http://' + url,
                    'revision_id': '1.0',
                    'description': 'This is a resource for sensor, ' + sensor_name,
                    'format': 'JSON',
                    'name': 'sensor_' + sensor_name + '_resource'
                }
                resource_created = ckan_api.ckan_api(url, api_key, action, data_dict)
                # 2. datastore_create
                action = 'datastore_create'
                fields = [
                    {'id': 'sensor_value', 'type': 'text'},
                    {'id': 'sensor_unit', 'type': 'text'},
                    {'id': 'datetime', 'type': 'timestamp'},
                    {'id': 'longitude', 'type': 'text'},
                    {'id': 'latitude', 'type': 'text'}
                ]
                records = [{
                    'sensor_value': sensor1['sensor_value'],
                    'sensor_unit': sensor1['sensor_unit'],
                    'datetime': sensor1['datetime'],
                    'longitude': sensor1['longitude'],
                    'latitude': sensor1['latitude']
                }]
                data_dict = {
                    'resource_id': resource_created['id'],
                    'force': True,
                    'fields': fields,
                    'records': records
                }
                ckan_api.ckan_api(url, api_key, action, data_dict)
                # 3. resource_update
                action = 'resource_update'
                data_dict = {
                    'id': resource_created['id'],
                    'url': 'http://' + url + '/datastore/dump/' + resource_created['id']
                }
                ckan_api.ckan_api(url, api_key, action, data_dict)
                # 4. datastore_upsert
                action = 'datastore_upsert'
                records = [{
                    'sensor_uuid': sensor_uuid,
                    'sensor_name': sensor_name,
                    'sensor_type': sensor_type,
                    'sensor_resource_uuid': resource_created['id'].encode('UTF-8'),
                    'sensor_resource_name': resource_created['name'].encode('UTF-8')
                }]
                data_dict = {
                    'resource_id': gateway_resource_uuid,
                    'force': True,
                    'records': records,
                    'method': 'insert'
                }
                ckan_api.ckan_api(url, admin_api_key, action, data_dict)

                print '    sensor ' + sensor_name + 'complete registration'

    else:   # gateway not registered, register gateway first

        print 'gateway ' + gateway_name + ' not register'
        print 'gateway ' + gateway_name + ' start registering'

        # 1.1 resource_create [gateway name]_sensors_resource
        action = 'resource_create'
        data_dict = {
            'package_id': gateways_dataset_uuid,
            'url': 'http://' + url,
            'revision_id': '1.0',
            'description': 'This is a sensor aggregation resource of gateway, ' + gateway_name,
            'format': 'JSON',
            'name': gateway_name + '_sensors_resource'
        }
        resource_created = ckan_api.ckan_api(url, admin_api_key, action, data_dict)
        gateway_resource_uuid = resource_created['id']
        gateway_resource_name = gateway_name + '_sensors_resource'
        # 1.2 datastore_create
        action = 'datastore_create'
        fields = [
            {'id': 'sensor_uuid', 'type': 'text'},
            {'id': 'sensor_name', 'type': 'text'},
            {'id': 'sensor_type', 'type': 'text'},
            {'id': 'sensor_resource_uuid', 'type': 'text'},
            {'id': 'sensor_resource_name', 'type': 'text'}
        ]
        data_dict = {
            'resource_id': gateway_resource_uuid,
            'force': True,
            'fields': fields,
        }
        ckan_api.ckan_api(url, admin_api_key, action, data_dict)
        # 1.3 resource_update
        action = 'resource_update'
        data_dict = {
            'id': gateway_resource_uuid,
            'url': 'http://' + url + '/datastore/dump/' + gateway_resource_uuid
        }
        ckan_api.ckan_api(url, admin_api_key, action, data_dict)

        # 2. package_create [gateway name]_dataset
        action = 'package_create'
        gateway_dataset_name = 'gateway_' + gateway_uuid.lower() + '_dataset'
        data_dict = {
            'name': gateway_dataset_name,
            'title': 'gateway_' + gateway_name + '_dataset',
            'notes': 'This is a dataset for gateway, ' + gateway_name
        }
        dataset_created = ckan_api.ckan_api(url, api_key, action, data_dict)
        gateway_dataset_uuid = dataset_created['id']

        # 3. for every sensor to do, it is same as ...
        for sensor in sensor_list:
            sensor_uuid = sensor['sensor_uuid']
            sensor_name = sensor['sensor_name']
            sensor_type = sensor['sensor_type']

            print '    sensor ' + sensor_name + ' start registering'

            # 3.1 resource_create [sensor name]_resource
            action = 'resource_create'
            data_dict = {
                'package_id': gateway_dataset_uuid,
                'url': 'http://' + url,
                'revision_id': '1.0',
                'description': 'This is a resource for sensor, ' + sensor_name,
                'format': 'JSON',
                'name': 'sensor_' + sensor_name + '_resource'
            }
            resource_created = ckan_api.ckan_api(url, api_key, action, data_dict)
            # 3.2. datastore_create
            action = 'datastore_create'
            fields = [
                {'id': 'sensor_value', 'type': 'text'},
                {'id': 'sensor_unit', 'type': 'text'},
                {'id': 'datetime', 'type': 'timestamp'},
                {'id': 'longitude', 'type': 'text'},
                {'id': 'latitude', 'type': 'text'}
            ]
            records = [{
                'sensor_value': sensor['sensor_value'],
                'sensor_unit': sensor['sensor_unit'],
                'datetime': sensor['datetime'],
                'longitude': sensor['longitude'],
                'latitude': sensor['latitude']
            }]
            data_dict = {
                'resource_id': resource_created['id'],
                'force': True,
                'fields': fields,
                'records': records
            }
            ckan_api.ckan_api(url, api_key, action, data_dict)
            # 3.3 resource_update
            action = 'resource_update'
            data_dict = {
                'id': resource_created['id'],
                'url': 'http://' + url + '/datastore/dump/' + resource_created['id']
            }
            ckan_api.ckan_api(url, api_key, action, data_dict)
            # 3.4 datastore_upsert
            action = 'datastore_upsert'
            records = [{
                'sensor_uuid': sensor_uuid,
                'sensor_name': sensor_name,
                'sensor_type': sensor_type,
                'sensor_resource_uuid': resource_created['id'].encode('UTF-8'),
                'sensor_resource_name': resource_created['name'].encode('UTF-8')
            }]
            data_dict = {
                'resource_id': gateway_resource_uuid,
                'force': True,
                'records': records,
                'method': 'insert'
            }
            ckan_api.ckan_api(url, admin_api_key, action, data_dict)

            print '    sensor ' + sensor_name + ' complete registration'

        # 4. datastore_upsert the gateways_resource
        action = 'datastore_upsert'
        records = [{
            'gateway_uuid': gateway_uuid.encode('UTF-8'),
            'gateway_name': gateway_name.encode('UTF-8'),
            'gateway_resource_uuid': gateway_resource_uuid.encode('UTF-8'),
            'gateway_resource_name': gateway_resource_name.encode('UTF-8'),
            'gateway_dataset_uuid': gateway_dataset_uuid.encode('UTF-8'),
            'gateway_dataset_name': gateway_dataset_name.encode('UTF-8'),
            'gateway_owner_api_key': api_key
        }]
        data_dict = {
            'resource_id': gateways_resource_uuid,
            'force': True,
            'records': records,
            'method': 'insert'
        }
        ckan_api.ckan_api(url, admin_api_key, action, data_dict)

        print 'gateway ' + gateway_name + ' complete registration'

    end_datetime = str(datetime.datetime.now().isoformat())
    print '[end] success ' + end_datetime

client = mqtt.Client()
client.username_pw_set(broker_username, broker_password)

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_url, broker_port, 60)

print 'Awaiting...'

client.loop_forever()

