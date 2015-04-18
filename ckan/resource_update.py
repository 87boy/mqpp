
import ckan_api
from config import *

action = 'resource_update'
resource_id = 'a816af3e-4a3b-49f6-809f-3a2cad839dd6'
data_dict = {
    'id': resource_id,
    'url': 'http://' + url + '/datastore/dump/' + resource_id
}

result = ckan_api.ckan_api_man(url, admin_api_key, action, data_dict)
print(result)
