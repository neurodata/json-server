import requests
import json

base_url = 'https://json.neurodata.io/v1'

# test a simple GET request

url = '{}?NGStateID=b8rw7q2DrhUOiw'.format(base_url)
headers = {'Content-type': 'application/json'}
r = requests.get(url, headers=headers)
print(r.json())


with open('large_state.json', 'r') as jsonfile:
    payload = json.load(jsonfile)

r = requests.post(url, json=payload)
print(r.json())
