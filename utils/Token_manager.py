import boto3
import json
import requests
import time

class TokenManager:
    def __init__(self, secret_name, region_name="us-east-1"):
        self.secret_name = secret_name
        self.region_name = region_name
        self.token = None
        self.token_expiry = 0  # Unix timestamp when token expires

    def get_secret(self):
        client = boto3.client("secretsmanager", region_name=self.region_name)
        response = client.get_secret_value(SecretId=self.secret_name)
        return json.loads(response["SecretString"])

    def get_access_token(self):
        current_time = int(time.time())
        
        # If token exists and not expired → reuse it
        if self.token and current_time < self.token_expiry:
            return self.token

        # Else → fetch a new token
        secrets = self.get_secret()
        client_id = secrets["client_id"]
        client_secret = secrets["client_secret"]

        token_url = "https://example.com/oauth2/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }

        retries = 3
        for attempt in range(retries):
            try:
                response = requests.post(token_url, data=payload, timeout=10)
                response.raise_for_status()
                data = response.json()

                # Store token and calculate expiry
                self.token = data["access_token"]
                expires_in = data.get("expires_in", 3600)  # fallback = 1 hour
                self.token_expiry = current_time + expires_in - 30  # refresh 30s before expiry
                return self.token

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Token request failed (attempt {attempt+1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # exponential backoff
                else:
                    raise RuntimeError("❌ Failed to retrieve access token after retries")

    def get_auth_headers(self):
        token = self.get_access_token()
        return {"Authorization": f"Bearer {token}"}
