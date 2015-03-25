
import ckan_api
from config import *

action = 'package_show'
data_dict = {
    'id': 'gateways-dataset'
}

result = ckan_api.ckan_api_man(url, admin_api_key, action, data_dict)
print(result)
