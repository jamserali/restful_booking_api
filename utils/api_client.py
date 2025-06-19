import json
import boto3
import requests
from config.environment_config import ActiveConfig
from data.payloads import get_access_token_payload
from endpoints.booking_endpoints import BookingEndpoints
from utils.aws_secrets import AWSSecretManager


class APIClient:
    def __init__(self):
        self.base_url = ActiveConfig.BASE_URL
        self.timeout = ActiveConfig.TIMEOUT
        self.auth_token = None

    # Implemented AWS Secret manager to get client secret and client_id
    def make_authenticated_request(self, method, url, headers=None, payload=None, retries=1):
        if headers is None:
            headers = {}

        # Always refresh header with current token
        headers["Authorization"] = f"Bearer {self.auth_token}"
        response = requests.request(method=method, url=url, headers=headers, json=payload)

        # Handle token expiration
        if response.status_code == 401 and retries > 0:
            print("Token expired. Refreshing...")
            self.auth_token = AWSSecretManager.get_access_token()
            return self.make_authenticated_request(method, url, headers, payload, retries - 1)
        return response

    # Regular CRUD methods

    def post(self, url, headers=None, json=None):
        return requests.post(
            url,
            headers=headers,
            json=json,
            timeout=self.timeout
        )

    def get(self, url, headers=None):
        return requests.get(
            url,
            headers=headers,
            timeout=self.timeout
        )

    def put(self, url, headers=None, json=None):
        return requests.put(
            url,
            headers=headers,
            json=json,
            timeout=self.timeout
        )

    def patch(self, url, headers=None, json=None):
        return requests.patch(
            url,
            headers=headers,
            json=json,
            timeout=self.timeout
        )

    def delete(self, url, headers=None):
        return requests.delete(
            url,
            headers=headers,
            timeout=self.timeout
        )
