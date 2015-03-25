
import ckan_api
from config import *

action = 'datastore_upsert'

records = [{
    'gateway_uuid':'42345678-1234-1234-1234-123456789012',
    'gateway_name': 'FYLZ04',
    'gateway_resource_uuid': 'd3196a96-fa06-425d-91f5-311dca7f6131',
    'gateway_resource_name': 'FYLZ03_sensors_resource',
    'gateway_dataset_uuid': 'dfbe943a-d5b9-4cd9-b2a1-5f386ff8b74d',
    'gateway_dataset_name': 'FYLZ03_dataset'
}]

data_dict = {
    'resource_id': '67a762a2-b429-4e21-ab42-159f8448c06d',
    'force': True,
    'records': records,
    'method': 'insert'
}

result = ckan_api.ckan_api_man(url, admin_api_key, action, data_dict)
print(result)
