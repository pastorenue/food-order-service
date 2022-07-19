from asyncio.log import logger
from typing import Dict

from backend_api.api_clients import NourishMeAPIClient
from backend_api.config import BASE_API_URL


class CustomerDataMapper:

    def __init__(self, data: Dict) -> None:
        self.data = data
        self.client = NourishMeAPIClient(BASE_API_URL)
    
    @property
    def address(self) -> Dict:
        address = self.data["Address"]
        return {
            "street": address.get("Street"),
            "city": address.get("City"),
            "postal_code": address.get("PostalCode")
        }

    @property
    def dishes(self):
        orders = self.data.get("Order").split(',')
        order_list = [order.partition('x') for order in orders]

        try:
            menu = self.client.get_menu_list()
        except ConnectionError:
            logger.error("Connection Error") # Not the regular error logging

        return [
            {
                "dish_id": menu[order[2].lstrip().rstrip()],
                "amount": order[0]
            }
            for order in order_list
        ]
    
    def as_dict(self) -> Dict:
        return {
            "customer": {
                "full_name": self.data.get("Name"),
                "address": self.address,
            },
            "dishes": self.dishes
        }