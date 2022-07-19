from copy import deepcopy
import json
from logging import getLogger
from typing import Dict, Optional

from backend_api.config import (
    BASE_API_URL,
    CLIENT_API_KEY,
    DEFAULT_TIMEOUT,
)
import requests

logger = getLogger(__name__)
request = requests.Session()


BASE_API_URL = BASE_API_URL


class APIError(Exception):
    """Error that indicates that data request failed"""


class BaseAPIClient:
    """
    Base API Client

    This is serving as a base api client wrapper.
    This can be extended by other resources
    """

    versions = {
        "v1": "",
        "v2": "api/v2",
    }
    default_version = "v1"

    def __init__(self, api_url, timeout: float=DEFAULT_TIMEOUT) -> None:
        self.api_url = api_url
        self.timeout = timeout
    
    @property
    def client_api_key(self):
        """API token"""
        return CLIENT_API_KEY
    
    def _get_url(self, endpoint: str) -> str:
        """Returns a formatted url"""
        return f"{BASE_API_URL}/{self.default_version}/{endpoint}"
    
    def _headers(self) -> Dict:
        """Returns headers required by API"""
        return {
            "token": self.client_api_key, # This is fictitious hoping the api is secured
            "Content-Type": "application/json",
        }
    
    def _get(self, endpoint: str=None, **kwargs) -> Dict:
        """Makes a get request to the API"""
        url = self._get_url(endpoint)
        return request.get(
            url,
            headers=self._headers(),
            timeout=DEFAULT_TIMEOUT,
            params=kwargs
        ).json()
    
    def _post(
        self,
        endpoint:  str=None,
        data: Dict=None
    ) -> Optional[Dict]:
        """Makes a post request to the API"""
        url = self._get_url(endpoint)
        try:
            return request.post(url, data=data, headers=self._headers)
        except ConnectionError as e:
            logger.error(f"Error: {str(e)}")
        return {
            "details": "Error" # Not the regular error
        }


class NourishMeAPIClient(BaseAPIClient):

    def __init__(
        self,
        api_url,
        timeout: float = DEFAULT_TIMEOUT
    ) -> None:
        super(NourishMeAPIClient, self).__init__(api_url, timeout)
    
    def get_menu_list(self) -> Optional[Dict]:
        """Request menue list from the nourish.me API"""
        result = {}
        try:
            result = self._get('menu')
        except APIError as e:
            logger.error(f"Error occurred: {str(e)}")
        finally: # TODO: Remove after testing
            with open("data/menu.json", "r") as f:
                result = json.loads(f.read())

        return self._process_json_response(result)
    
    def _process_json_response(self, data: Dict) -> Dict:
        """Transform API response into annotated data object"""
        if _data := deepcopy(data):
            dishes = _data.get("dishes", {})

        return {
            name: idx
            for idx, name in dishes.items()
        }

    def place_order(self, data: Dict, is_bulk=True) -> Optional[Dict]:
        """Place order"""
        endpoint = "bulk/order" if is_bulk else "..." # TODO: for a single order
        return  self._post(endpoint, data=data)