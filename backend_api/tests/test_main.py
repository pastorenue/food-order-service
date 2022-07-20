import requests
from fastapi.testclient import TestClient
from backend_api.main import app

client = TestClient(app)


def test_main():
    response = client.get('/')
    assert response.status_code == requests.codes.ok
