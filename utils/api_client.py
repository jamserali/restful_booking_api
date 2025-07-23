import json
import boto3
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from config.environment_config import ActiveConfig
from data.payloads import get_access_token_payload
from endpoints.booking_endpoints import BookingEndpoints


class APIClient:
    def __init__(self):
        self.base_url = ActiveConfig.BASE_URL
        self.timeout = ActiveConfig.TIMEOUT
        self.session = requests.Session()
        self.retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=self.retries))
        # self.auth_token = None

    def post(self, url, headers=None, json=None):
        """Send a POST request with retries and timeout."""
        try:
            response = self.session.post(
                f"{self.base_url}{url}",
                headers=headers,
                json=json,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    def get(self, url, headers=None):
        return self.session.get(
            f"{self.base_url}{url}",
            headers=headers,
            timeout=self.timeout
        )

    def put(self, url, headers=None, json=None):
        return self.session.put(
            f"{self.base_url}{url}",
            headers=headers,
            json=json,
            timeout=self.timeout
        )

    def delete(self, url, headers=None):
        return self.session.delete(
            f"{self.base_url}{url}",
            headers=headers,
            timeout=self.timeout
        )

    # Implemented AWS Secret manager to get client secret and client_id
    def get_secret(self, secret_name, region_name="us-east-1"):
        client = boto3.client("secretsmanager", region_name)
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret = json.loads(response["SecretString"])
            return secret

    def get_access_token(self):
        secret_data = self.get_secret("Secret_name")
        client_id = secret_data["client_id"]
        client_secret = secret_data["client_secret"]
        response = requests.post(BookingEndpoints.auth(),
                                 json=get_access_token_payload(client_id, client_secret))
        return response.json()["access_token"]

    def make_authenticated_request(self, method, url, headers=None, payload=None, retries=1):
        if headers is None:
            headers = {}

        # Always refresh header with current token
        headers["Authorization"] = f"Bearer {self.auth_token}"

        response = requests.request(method=method, url=url, headers=headers, json=payload)

        # Handle token expiration
        if response.status_code == 401 and retries > 0:
            print("Token expired. Refreshing...")
            self.auth_token = self.get_access_token()
            return self.make_authenticated_request(method, url, headers, payload, retries - 1)
        return response
