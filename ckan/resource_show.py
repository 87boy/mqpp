
import ckan_api
from config import *

action = 'resource_show'
resource_id = '4d9fae79-b929-4871-9b87-a598e3968f2f'
data_dict = {
    'id': resource_id,
}

result = ckan_api.ckan_api_man(url, api_key, action, data_dict)
print(result)
