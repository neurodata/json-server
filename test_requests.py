import requests
import json

base_url = 'https://json.neurodata.io/v1'

# test POST request (ID should exist in DB)
with open('large_state.json', 'r') as jsonfile:
    payload = json.load(jsonfile)
r = requests.post(base_url, json=payload)
print('POST response:', r.json())

queryparam = r.json()['uri'].split('?')[1]


# test GET request (ID should exist in DB)
headers = {'Content-type': 'application/json'}
url = '{}?{}'.format(base_url, queryparam)
r = requests.get(url, headers=headers)
print('GET response:', r.json())


assert(r.json() == payload)
