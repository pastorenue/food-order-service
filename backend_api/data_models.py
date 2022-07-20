from copy import deepcopy
import json
from logging import getLogger
from typing import Dict, List

from backend_api.api_clients import NourishMeAPIClient
from backend_api.config import BASE_API_URL


class CustomerDataMapper:

    def __init__(self, data: Dict) -> None:
        self.data = data
        self.logger = getLogger(__name__)
        self.client = NourishMeAPIClient(BASE_API_URL, logger=self.logger)
    
    @property
    def address(self) -> Dict:
        address = self.data["Address"]
        return {
            "street": address.get("Street"),
            "city": address.get("City"),
            "postal_code": address.get("PostalCode")
        }

    @property
    def dishes(self) -> List:
        orders = self.data.get("Order").split(',')
        order_list = [order.partition('x') for order in orders]

        try:
            menu = self.client.get_menu_list
        except ConnectionError:
            self.logger.error("Connection Error") # Not the regular error logging

        if not menu:
            with open("data/menu.json", "r") as f:
                menu = self._process_json_response(
                    json.loads(f.read())
                )
        
        return [
            {
                "dish_id": menu.get(order[2].lstrip().rstrip()),
                "amount": order[0]
            }
            for order in order_list
        ]
    
    def _process_json_response(self, data: Dict) -> Dict:
        """Transform API response into annotated data object"""
        if _data := deepcopy(data):
            dishes = _data.get("dishes", {})

        return {
            dish.get("name"): dish.get("id")
            for dish in dishes
            if dish
        }
        
    
    def as_dict(self) -> Dict:
        return {
            "customer": {
                "full_name": self.data.get("Name"),
                "address": self.address,
            },
            "dishes": self.dishes
        }