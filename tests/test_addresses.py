from fastapi import status
from fastapi.testclient import TestClient

from projeto_final_poo.db.models import Client


def test_add_address(test_client: TestClient, client: Client):
    response = test_client.post(
        '/address/',
        json={
            'client_id': client.id,
            'street': 'Flower Street',
            'neighborhood': 'Central District',
            'reference': 'Near the Park',
            'number': '123',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': 2,
        'client_id': client.id,
        'street': 'Flower Street',
        'neighborhood': 'Central District',
        'reference': 'Near the Park',
        'number': '123',
    }


def test_add_address_to_non_existing_client(test_client: TestClient):
    response = test_client.post(
        '/address/',
        json={
            'client_id': 999,
            'street': 'Flower Street',
            'neighborhood': 'Central District',
            'reference': 'Near the Park',
            'number': '123',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Client not found'}


def test_get_addresses_by_client(test_client: TestClient, client: Client):
    response = test_client.get(f'/address/{client.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'addresses': [
            {
                'id': client.addresses[0].id,
                'street': client.addresses[0].street,
                'neighborhood': client.addresses[0].neighborhood,
                'reference': client.addresses[0].reference,
                'number': client.addresses[0].number,
            }
        ]
    }


def test_get_addresses_by_non_existing_client(test_client: TestClient):
    response = test_client.get('/address/999')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Client not found'}


def test_update_address(test_client: TestClient, client: Client):
    response = test_client.put(
        f'/address/{client.addresses[0].id}',
        json={
            'street': 'Updated Street',
            'neighborhood': 'Updated District',
            'reference': 'Updated Reference',
            'number': '456',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': client.addresses[0].id,
        'client_id': client.addresses[0].client_id,
        'street': 'Updated Street',
        'neighborhood': 'Updated District',
        'reference': 'Updated Reference',
        'number': '456',
    }


def test_update_non_existing_address(test_client: TestClient):
    response = test_client.put(
        '/address/999',
        json={
            'street': 'Updated Street',
            'neighborhood': 'Updated District',
            'reference': 'Updated Reference',
            'number': '456',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Address not found'}


def test_delete_address(test_client: TestClient, client: Client):
    response = test_client.delete(f'/address/{client.addresses[0].id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Address deleted'}


def test_delete_non_existing_address(test_client: TestClient):
    response = test_client.delete('/address/999')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Address not found'}
