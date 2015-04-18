
import ckan_api
from config import *

action = 'datastore_search'
data_dict = {
    'resource_id': '67a762a2-b429-4e21-ab42-159f8448c06d'
}

result = ckan_api.ckan_api(url, admin_api_key, action, data_dict)
print(result)
