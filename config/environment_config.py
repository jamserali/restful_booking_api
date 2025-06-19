from .base_config import BaseConfig


class DevConfig(BaseConfig):
    ENV = "DEV"
    USERNAME = "admin"
    PASSWORD = "password123"


class StagingConfig(BaseConfig):
    ENV = "STAGING"
    USERNAME = "admin"
    PASSWORD = "password123"


class ProdConfig(BaseConfig):
    ENV = "PROD"
    USERNAME = "admin"
    PASSWORD = "password123"


class QAConfig(BaseConfig):
    ENV = "QA"
    USERNAME = "admin"
    PASSWORD = "password123"


# Set active configuration
ActiveConfig = QAConfig  # Change this to switch environments
