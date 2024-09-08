from fastapi import status
from fastapi.testclient import TestClient

from projeto_final_poo.schemas.schemas import ServicePublic


def test_create_service(test_client: TestClient):
    response = test_client.post(
        '/services',
        json={
            'type': 'Cleaning',
            'description': 'Deep cleaning service',
            'price': 99.99,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': 1,
        'type': 'Cleaning',
        'description': 'Deep cleaning service',
        'price': 99.99,
    }


def test_get_services_empty(test_client: TestClient):
    response = test_client.get('/services')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'services': []}


def test_get_services_with_services(
    test_client: TestClient, service, other_service
):
    service_schema = ServicePublic.model_validate(service).model_dump()
    other_service_schema = ServicePublic.model_validate(
        other_service
    ).model_dump()

    response = test_client.get('/services')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'services': [service_schema, other_service_schema]
    }


def test_get_service_by_id(test_client: TestClient, service):
    service_schema = ServicePublic.model_validate(service).model_dump()
    response = test_client.get(f'/services/{service.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == service_schema


def test_get_not_found_service_by_id(test_client: TestClient, service):
    response = test_client.get(f'/services/{service.id + 1}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Service not found'}


def test_update_service(test_client: TestClient, service):
    response = test_client.put(
        f'/services/{service.id}',
        json={
            'type': 'Updated Service',
            'description': 'Updated description',
            'price': 129.99,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'type': 'Updated Service',
        'description': 'Updated description',
        'price': 129.99,
    }


def test_update_not_found_service(test_client: TestClient, service):
    response = test_client.put(
        f'/services/{service.id + 1}',
        json={
            'type': 'Updated Service',
            'description': 'Updated description',
            'price': 129.99,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Service not found'}


def test_delete_service(test_client: TestClient, service):
    response = test_client.delete(f'/services/{service.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Service deleted'}


def test_delete_not_found_service(test_client: TestClient, service):
    response = test_client.delete(f'/services/{service.id + 1}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Service not found'}
