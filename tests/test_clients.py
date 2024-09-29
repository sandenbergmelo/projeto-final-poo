from fastapi import status
from fastapi.testclient import TestClient

from projeto_final_poo.db.models import Client
from projeto_final_poo.schemas.schemas import ClientPublic


def test_create_client(test_client: TestClient):
    response = test_client.post(
        '/clients',
        json={
            'name': 'John Doe',
            'phone_number': '+5588999999999',
            'street': 'Flower Street',
            'neighborhood': 'Central District',
            'reference': 'Flat 102',
            'number': '456',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': 1,
        'name': 'John Doe',
        'phone_number': '+5588999999999',
        'addresses': [
            {
                'id': 1,
                'street': 'Flower Street',
                'neighborhood': 'Central District',
                'reference': 'Flat 102',
                'number': '456',
            }
        ],
    }


def test_create_user_phone_number_already_exists(
    test_client: TestClient, client: Client
):
    response = test_client.post(
        '/clients',
        json={
            'name': 'John Doe again',
            'phone_number': client.phone_number,
            'street': 'Flower Street',
            'neighborhood': 'Central District',
            'reference': 'Flat 102',
            'number': '456',
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        'detail': 'Phone number already exists in another client'
    }


def test_get_clients_empty(test_client: TestClient):
    response = test_client.get('/clients')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'clients': []}


def test_get_clients_with_clients(
    test_client: TestClient, client, other_client
):
    user_schema = ClientPublic.model_validate(client).model_dump()
    other_user_schema = ClientPublic.model_validate(other_client).model_dump()

    response = test_client.get('/clients')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'clients': [user_schema, other_user_schema]}


def test_get_client_by_id(test_client: TestClient, client):
    user_schema = ClientPublic.model_validate(client).model_dump()
    response = test_client.get(f'/clients/{client.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user_schema


def test_get_not_found_client_by_id(test_client: TestClient, client):
    response = test_client.get(f'/clients/{client.id + 1}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Client not found'}


def test_update_client(test_client: TestClient, client):
    response = test_client.put(
        f'/clients/{client.id}',
        json={
            'name': 'John Doe',
            'phone_number': '+5588999999999',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'name': 'John Doe',
        'phone_number': '+5588999999999',
        'addresses': [
            {
                'id': client.addresses[0].id,
                'street': client.addresses[0].street,
                'neighborhood': client.addresses[0].neighborhood,
                'reference': client.addresses[0].reference,
                'number': client.addresses[0].number,
            }
        ],
    }


def test_update_client_with_same_phone_number(
    test_client: TestClient, client, other_client
):
    response = test_client.put(
        f'/clients/{client.id}',
        json={
            'name': 'John Doe',
            'phone_number': other_client.phone_number,
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        'detail': 'Phone number already exists in another client'
    }


def test_update_not_found_client(test_client: TestClient, client):
    response = test_client.put(
        f'/clients/{client.id + 1}',
        json={
            'name': 'John Doe',
            'phone_number': '+5588999999999',
            'street': 'Flower Street',
            'neighborhood': 'Central District',
            'reference': 'Flat 102',
            'number': '456',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Client not found'}


def test_delete_client(test_client: TestClient, client):
    response = test_client.delete(f'/clients/{client.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'message': 'Client and associated addresses deleted'
    }


def test_delete_not_found_client(test_client: TestClient, client):
    response = test_client.delete(f'/clients/{client.id + 1}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Client not found'}
