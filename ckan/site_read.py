
import ckan_api
from config import *

action = 'site_read'
data_dict = {
}

result = ckan_api.ckan_api_man(url, fake_api_key, action, data_dict)
print(result)
