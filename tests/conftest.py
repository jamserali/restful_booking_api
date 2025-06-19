import pytest
from data.headers import Headers
from utils.api_client import APIClient
from data.payloads import get_auth_payload
from endpoints.booking_endpoints import BookingEndpoints
from utils.aws_secrets import AWSSecretManager


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope="session")
def aws_secrets():
    """Fixture to verify AWS secrets are accessible"""
    try:
        secret = AWSSecretManager.get_secret("Secret_name")
        assert secret is not None
        return secret
    except Exception as e:
        pytest.skip(f"AWS Secrets not available: {str(e)}")


@pytest.fixture
def aws_auth_token(aws_secrets):
    """Fixture to get auth token (already handled by APIClient)"""
    return AWSSecretManager.get_access_token()


@pytest.fixture
def auth_token(api_client):
    response = api_client.post(
        BookingEndpoints.auth(),
        headers=Headers.get_auth_headers(),
        json=get_auth_payload()
    )
    assert response.status_code == 200
    return response.json()["token"]
