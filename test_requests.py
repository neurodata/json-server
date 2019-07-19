import requests
import json

BASE_URL = "https://json.neurodata.io"
HEADERS = {"Content-type": "application/json"}


def test_post_v1():
    stage = "v1"

    # test POST request (ID should exist in DB)
    with open("large_state.json", "r") as jsonfile:
        payload = json.load(jsonfile)
    r = requests.post(f"{BASE_URL}/{stage}", json=payload)
    assert r.status_code == 201

    post_response = r.json()
    get_url = post_response["uri"]

    get_response = requests.get(get_url, headers=HEADERS)
    get_data = get_response.json()
    assert get_data == payload


def test_post_post():
    stage = "post"

    # ensure this data is in the db
    simple_dict = {"some_key": "some value"}
    r = requests.post(f"{BASE_URL}/{stage}", json=simple_dict)
    assert r.status_code == 201

    return_id = r.json().split("?")[1]

    # test GET request (ID should exist in DB)
    url = f"{BASE_URL}/{stage}?{return_id}"
    r = requests.get(url, headers=HEADERS)
    # print("GET response:", r.json())
    response = r.json()
    assert response == simple_dict
