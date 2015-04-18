
import ckan_api
from config import *

action = 'user_list'
data_dict = {
}

result = ckan_api.ckan_api_man(url, api_key, action, data_dict)
print(result)
