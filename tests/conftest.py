import pytest
from fastapi.testclient import TestClient

from projeto_final_poo.app import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
