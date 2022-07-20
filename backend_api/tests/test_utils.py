import pytest
from backend_api.utils import (
    _xml_to_dict,
    format_order_request_body
)


@pytest.fixture
def xml_file():
    """Test fixture with a dummy xml object"""
    return """
    <note>
        <to>Tove</to>
        <from>Jani</from>
        <heading>Reminder</heading>
        <body>Don't forget me this weekend!</body>
    </note>
    """

@pytest.fixture
def employee_test_file():
    """Test fixture with a real xml file"""
    return "backend_api/tests/employee.xml" # just returning the name of the file


def test_xml_to_dict(xml_file):
    """Test that the xml object is converted
    to a dictionary object
    """
    result = _xml_to_dict(xml_file)
    assert type(result) == dict
    assert "note" in result.keys()


def test_xml_to_dict_from_file(employee_test_file):
    """Test that the xml file is converted
     to a dictionary object
    """
    with open(employee_test_file, 'r') as f:
        result = _xml_to_dict(f.read())
    
    employees = result["Employees"]["Employee"]
    assert type(result) == dict
    assert len(employees) == 2
    assert employees[0]["Name"] == "Employee A"


def test_format_order_request_body(employee_test_file):
    """Test that the xml file passed is formatted
    to the format `NourishMe API expects
    """
    with open(employee_test_file, 'r') as f:
        result = format_order_request_body(f.read())
    
    assert type(result) == dict

    orders = result["orders"]
    assert len(orders) == 2

    # assert that second employee orders two dishes
    assert len(orders[1]["dishes"]) == 2
