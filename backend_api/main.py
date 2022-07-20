from backend_api.api_clients import NourishMeAPIClient
from backend_api.config import (
    BASE_API_URL,
    DEBUG
)
from backend_api.utils import _data_order_request_body

from fastapi import FastAPI


app = FastAPI(debug=DEBUG)

@app.get("/")
def index():
    """Makes request to the nourish.me API to  place the order"""

    # TODO: We can have a frontend side of things to receive the file
    # rather than hardcode it here. But for now, the xml file has to be
    # saved in the data directory 
    with open("data/employee_orders.xml", "r") as f:
        request_data = _data_order_request_body(f.read())
    
    client = NourishMeAPIClient(BASE_API_URL)

    # place the order
    return client.place_order(request_data)
