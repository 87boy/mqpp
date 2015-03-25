
import ckan_api
from config import *

action = 'package_create'
data_dict = {
    'name': 'gateways_dataset',
    'notes': 'This is a special dataset including gateway aggregation resource and sensor aggregation resources of every gateway.'
}

result = ckan_api.ckan_api_man(url, api_key, action, data_dict)
print(result)
