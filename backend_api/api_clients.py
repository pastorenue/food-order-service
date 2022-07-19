from copy import deepcopy
import json
from logging import getLogger
from sqlite3 import adapt
from typing import Dict, Optional, Tuple

from backend_api.config import (
    BACKOFF_FACTOR,
    BASE_API_URL,
    CLIENT_API_KEY,
    DEFAULT_TIMEOUT,
    MAX_RETRIES,
    STATUS_FORCE_LIST,
)
import requests
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = getLogger(__name__)


def request_retry_session(
    retries: int=0,
    backoff_factor: float=None,
    status_forcelist: Tuple=None,
    session: Session=None
):
    retries = retries or MAX_RETRIES
    backoff_factor = backoff_factor or BACKOFF_FACTOR
    status_forcelist = status_forcelist or STATUS_FORCE_LIST
    session = session or Session()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    return session


class APIError(Exception):
    """Error that indicates that data request failed"""


class BaseAPIClient:
    """
    Base API Client

    This is serving as a base api client wrapper.
    This can be extended by other HTTP resources
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
        return request_retry_session().get(
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
            return request_retry_session().post(
                url,
                data=data,
                headers=self._headers()
            )
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
        except ConnectionError as e:
            logger.error(f"Error occurred: {str(e)}")
        finally: # TODO: Remove after testing
            with open("data/menu.json", "r") as f:
                result = json.loads(f.read())
            res = self._process_json_response(result)
            print(res)
            return res
    
    def _process_json_response(self, data: Dict) -> Dict:
        """Transform API response into annotated data object"""
        if _data := deepcopy(data):
            dishes = _data.get("dishes", {})

        return {
            dish["name"]: dish["id"]
            for dish in dishes
        }

    def place_order(self, data: Dict, is_bulk=True) -> Optional[Dict]:
        """Place order"""
        endpoint = "bulk/order" if is_bulk else "..." # TODO: for a single order
        try:
            self._post(endpoint, data=data)
        except ConnectionError:
            logger.error("An error occurred")
        finally:
            return data