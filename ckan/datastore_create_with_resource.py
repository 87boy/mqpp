# this api does not work!

import ckan_api
from config import *

action = 'datastore_create'

resource = {
    'package_id': '4722a3fd-b9dd-46f0-91cf-4630757c66e2',
    'url': 'http://' + url,
    'revision_id': '1.0',
    'description': 'this is a resource for testing',
    'format': 'JSON',
    'name': 'test_resource'
}

fields = [
    {'id': 'gateway_uuid', 'type': 'text'},
    {'id': 'gateway_name', 'type': 'text'},
    {'id': 'gateway_resource_uuid', 'type': 'text'},
    {'id': 'gateway_resource_name', 'type': 'text'},
    {'id': 'gateway_dataset_uuid', 'type': 'text'},
    {'id': 'gateway_dataset_name', 'type': 'text'}
]

data_dict = {
    # 'resource_id': '67a762a2-b429-4e21-ab42-159f8448c06d',
    'force': True,
    'resource': resource,
    'fields': fields,
    'primary_key': 'gateway_uuid',
    'indexes': 'gateway_uuid'
}

result = ckan_api.ckan_api_man(url, admin_api_key, action, data_dict)
print(result)
