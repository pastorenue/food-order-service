from distutils.log import debug
import sys
from typing import Union
from backend_api.api_clients import NourishMeAPIClient
from backend_api.config import BASE_API_URL

from fastapi import FastAPI
from backend_api.utils import _data_order_request_body


app = FastAPI(debug=True)

@app.get("/")
def index():
    """Makes request to the nourish.me API to  place the order"""
    with open("data/employee_orders.xml", "r") as f:
        request_data = _data_order_request_body(f.read())
    
    client = NourishMeAPIClient(BASE_API_URL)

    # place the order
    return client.place_order(request_data)
