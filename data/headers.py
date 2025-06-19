from config.environment_config import ActiveConfig


class Headers:
    @staticmethod
    def get_auth_headers():
        return {
            "Content-Type": "application/json"
        }

    @staticmethod
    def get_json_headers(token=None):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
            headers["Cookie"] = f"token={token}"
        return headers
