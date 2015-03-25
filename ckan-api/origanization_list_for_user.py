
import ckan_api
from config import *

action = 'organization_list_for_user'
data_dict = {
    #'permission': 'create_dataset'
    #'all_fields': True
}

result = ckan_api.ckan_api_man(url, api_key, action, data_dict)
print(result)
