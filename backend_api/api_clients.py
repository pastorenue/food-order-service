from functools import cached_property
import logging

from typing import Dict, Optional, Tuple

import requests

from backend_api.config import (
    BACKOFF_FACTOR,
    BASE_API_URL,
    CLIENT_API_KEY,
    DEFAULT_TIMEOUT,
    MAX_RETRIES,
    STATUS_FORCE_LIST,
)
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

LOG_TEMPLATE = (
    "Food Order Service Request:\n"
    "API_URL={api_url}\n"
    "ENDPOINT={endpoint}\n"
    "VERSION={version}\n"
    "REQUEST_DATA:{request_data}\n"
)

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

    def __init__(self, api_url, timeout: float=DEFAULT_TIMEOUT, logger=None) -> None:
        self.api_url = api_url
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)
    
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
            response = request_retry_session().post(
                url,
                data=data,
                headers=self._headers()
            )
            # Log request details
            self.logger.info(
                self._log_message(
                    api_url=url,
                    request_data=data,
                    endpoint=endpoint,
                    version=self.default_version,
                    status=response.status_code
                )
            )
            return response
        except ConnectionError as e:
            self.logger.error(f"Error: {str(e)}")
        return {
            "details": "Error" # Not the best error handler
        }
    
    def _log_message(self, api_url, request_data, endpoint, version: str="v1"):
        """Format request information for logging"""
        return LOG_TEMPLATE.format(
            api_url=api_url,
            request_data=request_data,
            endpoint=endpoint,
            version=version,
        )


class NourishMeAPIClient(BaseAPIClient):

    def __init__(
        self,
        api_url,
        timeout: float = DEFAULT_TIMEOUT,
        logger = None
    ) -> None:
        super(NourishMeAPIClient, self).__init__(api_url, timeout, logger=logger)
    
    @cached_property
    def get_menu_list(self) -> Optional[Dict]:
        """Request menu list from the nourish.me API"""
        result = {}
        try:
            response = self._get('menu')
            if response.status_code == requests.codes.ok:
                result = response.json()
        except ConnectionError as e:
            self.logger.error(f"Error occurred: {str(e)}")
        finally: # TODO: Remove after testing
            return result

    def place_order(self, data: Dict, is_bulk=True) -> Optional[Dict]:
        """Place order"""
        endpoint = "bulk/order" if is_bulk else ... # TODO: for a single order
        data = {}

        try:
            response = self._post(endpoint, data=data)
            data = response.json()
        except ConnectionError:
            self.logger.error("An error occurred") # Not the best error handler
        finally:
            return data