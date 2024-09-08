from fastapi import status
from fastapi.testclient import TestClient


def test_root_should_return_200_and_hello_world(test_client: TestClient):
    response = test_client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Hello, World!'}
