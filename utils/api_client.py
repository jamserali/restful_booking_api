import requests
from config.environment_config import ActiveConfig

class APIClient:
    def __init__(self):
        self.base_url = ActiveConfig.BASE_URL
        self.timeout = ActiveConfig.TIMEOUT

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

    def delete(self, url, headers=None):
        return requests.delete(
            url,
            headers=headers,
            timeout=self.timeout
        )