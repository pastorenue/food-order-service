import os


BASE_API_URL = os.environ.get("BASE_API_URL", "https://nourish.me/api")
DEFAULT_TIMEOUT = 0.0003
CLIENT_API_KEY = os.environ.get("CLIENT_API_KEY", "123456")
MAX_RETRIES = 1
BACKOFF_FACTOR = 0.3
STATUS_FORCE_LIST = (500, 502, 504)
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")

DEBUG = ENVIRONMENT == "dev"