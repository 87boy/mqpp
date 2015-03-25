
import ckan_api
from config import *

action = 'package_delete'
data_dict = {
    'id': 'test_dataset',
}

result = ckan_api.ckan_api_man(url, api_key, action, data_dict)
print(result)
