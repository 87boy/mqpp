
import ckan_api
from config import *

action = 'user_show'
data_dict = {
    'user_obj': {
        'apikey': api_key
    }
}

result = ckan_api.ckan_api_man(url, api_key, action, data_dict)
print(result)
