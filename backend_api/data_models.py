from typing import Dict

from backend_api.api_clients import NourishMeAPIClient
from backend_api.config import BASE_API_URL


class CustomerDataMapper:

    def __init__(self, data: Dict) -> None:
        self.data = data
        self.client = NourishMeAPIClient(BASE_API_URL)
    
    @property
    def address(self) -> Dict:
        return {
            "street": self.data.get("Street"),
            "city": self.data.get("City"),
            "postal_code": self.data.get("PostalCode")
        }

    @property
    def dishes(self):
        order_string = self.data.get("Order")
        amount, _, name = order_string.partition('x')

        menu = self.client.get_menu_list()

        return {
            "dish_id": menu.get(name),
            "amount": amount
        }
    
    def as_dict(self) -> Dict:
        return {
            "customer": {
                "full_name": self.data.get("Name"),
                "address": self.address,
            },
            "dishes": [self.dishes]
        }