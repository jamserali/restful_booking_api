import json

def pretty_print(json_data):
    print(json.dumps(json_data, indent=2))

def validate_response(response, expected_status_code=200):
    assert response.status_code == expected_status_code, \
        f"Expected status {expected_status_code}, got {response.status_code}"
    return response.json()