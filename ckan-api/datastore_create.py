#!/usr/bin/python
# -*- coding: utf-8 -*-

import ckan_api
from config import *

action = 'datastore_create'

fields = [
    {'id': 'gateway_uuid', 'type': 'text'},
    {'id': 'gateway_name', 'type': 'text'},
    {'id': 'gateway_resource_uuid', 'type': 'text'},
    {'id': 'gateway_resource_name', 'type': 'text'},
    {'id': 'gateway_dataset_uuid', 'type': 'text'},
    {'id': 'gateway_dataset_name', 'type': 'text'},
    {'id': 'gateway_owner_api_key', 'type': 'text'}
]

data_dict = {
    'resource_id': 'a816af3e-4a3b-49f6-809f-3a2cad839dd6',
    'force': True,
    'fields': fields,
    # 'primary_key': 'gateway_uuid',
    # 'indexes': 'gateway_uuid'
}

result = ckan_api.ckan_api_man(url, admin_api_key, action, data_dict)
print(result)
