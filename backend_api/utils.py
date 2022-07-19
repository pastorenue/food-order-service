from copy import deepcopy
import json
from pprint import pprint
from typing import Dict
from xml.etree.ElementTree import XML 
import xmltodict

from backend_api.data_models import CustomerDataMapper


_xml = """
    <?xml version="1.0" encoding="utf-8"?>
    <Employees>
    <Employee>
    <Name>Max Mustermann</Name>
    <Address>
    <Street>Musterweg 3</Street>
    <City>Musterhausen</City>
    <PostalCode>12345</PostalCode>
    </Address>
    <Order>3x Pizza Quattro Formaggi</Order>
    <IsAttending>true</IsAttending>
    </Employee>
    </Employees>
    """
def _xml_to_dict(xml: XML) -> Dict:
    """Convert xml object to dictionary"""
    xml_object = xml or _xml
    obj = xmltodict.parse(xml_object)
    
    json_string = json.dumps(obj)
    return json.loads(json_string) # return a Dictionary


def _data_order_request_body(xml: XML) -> Dict:
    """Format data to order request body for our API call"""
    # Create a deep copy to avoid data modification
    data = _xml_to_dict(xml)

    request_data = deepcopy(data)
    print("Type", type(data))
    customers = [
        CustomerDataMapper(employee).as_dict()
        for employee in request_data["Employees"]["Employee"]
    ]

    return {
        "orders": customers
    }