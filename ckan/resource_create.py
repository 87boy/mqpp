
import ckan_api
from config import *

action = 'resource_create'
data_dict = {
    'package_id': '4722a3fd-b9dd-46f0-91cf-4630757c66e2',
    'url': 'http://' + url + '/dataset/dump/',
    'description': 'this is gateway aggregation resource',
    'format': 'JSON',
    'name': 'gateways_resource'
}

result = ckan_api.ckan_api_man(url, admin_api_key, action, data_dict)
print(result)
