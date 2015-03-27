#!/usr/bin/env python
# -*- coding=UTF-8 -*-

'''
    CKAN API
    @author: Bin Zhang
    @email: sjtuzb@gmail.com
'''

import json
import urllib
import urllib2

def ckan_api(url, api_key, action, data_dict):
    # Use the json module to dump the dictionary to a string for posting.
    data_string = urllib.quote(json.dumps(data_dict))
    # We'll use the package_create function to create a new dataset.
    request = urllib2.Request('http://' + url + '/api/3/action/' + action)
    # Creating a dataset requires an authorization header.
    request.add_header('Authorization', api_key)
    # Make the HTTP request.
    response = urllib2.urlopen(request, data_string)
    assert response.code == 200
    # Use the json module to load CKAN's response into a dictionary.
    response_dict = json.loads(response.read())
    assert response_dict['success'] is True
    # response's result
    result = response_dict['result']
    # Return the result.
    return result

def ckan_api_man(url, api_key, action, data_dict):
    # Use the json module to dump the dictionary to a string for posting.
    data_string = urllib.quote(json.dumps(data_dict))
    # We'll use the package_create function to create a new dataset.
    request = urllib2.Request('http://' + url + '/api/3/action/' + action)
    # Creating a dataset requires an authorization header.
    request.add_header('Authorization', api_key)
    # Make the HTTP request.
    response = urllib2.urlopen(request, data_string)
    assert response.code == 200
    # Use the json module to load CKAN's response into a dictionary.
    response_dict = json.loads(response.read())
    assert response_dict['success'] is True
    # Use the json module to load response's result into a json.
    result = json.dumps(response_dict['result'], sort_keys=True, indent=4)
    # Return the result.
    return result

