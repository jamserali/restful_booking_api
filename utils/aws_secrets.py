import json
import boto3
import requests

from config.base_config import BaseConfig
from data.payloads import get_access_token_payload
from endpoints.booking_endpoints import BookingEndpoints


class AWSSecretManager:

    # Implemented AWS Secret manager to get client secret and client_id
    @staticmethod
    def get_secret(region_name="us-east-1"):
        client = boto3.client("secretsmanager", region_name)
        response = client.get_secret_value(SecretId=BaseConfig.SECRET_NAME)
        if "SecretString" in response:
            secret = json.loads(response["SecretString"])
            return secret

    @staticmethod
    def get_access_token():
        secret_data = AWSSecretManager.get_secret(BaseConfig.SECRET_NAME)
        client_id = secret_data["client_id"]
        client_secret = secret_data["client_secret"]
        response = requests.post(BookingEndpoints.auth(),
                                 json=get_access_token_payload(client_id, client_secret))
        return response.json()["access_token"]
