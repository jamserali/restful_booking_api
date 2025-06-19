import pytest

from data.headers import Headers
from utils.api_client import APIClient
from data.payloads import get_auth_payload
from endpoints.booking_endpoints import BookingEndpoints

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_token(api_client):
    response = api_client.post(
        BookingEndpoints.auth(),
        headers=Headers.get_auth_headers(),
        json=get_auth_payload()
    )
    assert response.status_code == 200
    return response.json()["token"]

@pytest.fixture
def booking_id(api_client, auth_token):
    from data.payloads import get_booking_payload
    response = api_client.post(
        BookingEndpoints.booking(),
        headers=Headers.get_json_headers(),
        json=get_booking_payload()
    )
    assert response.status_code == 200
    return response.json()["bookingid"]
