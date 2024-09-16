import json

from fastapi import status
from fastapi.testclient import TestClient

from projeto_final_poo.schemas.schemas import SchedulePublic


def test_create_schedule(test_client: TestClient, client, service):
    response = test_client.post(
        '/schedules',
        json={
            'date': '2023-09-15',
            'shift': 'morning',
            'description': 'A scheduled maintenance service',
            'client_id': client.id,
            'service_id': service.id,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': 1,
        'date': '2023-09-15',
        'shift': 'morning',
        'description': 'A scheduled maintenance service',
        'client': {
            'id': client.id,
            'name': client.name,
        },
        'service': {
            'type': service.type,
        },
    }


def test_create_schedule_client_not_found(test_client: TestClient, service):
    response = test_client.post(
        '/schedules',
        json={
            'date': '2023-09-15',
            'shift': 'morning',
            'description': 'A scheduled maintenance service',
            'client_id': 999,
            'service_id': service.id,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Client not found'}


def test_create_schedule_service_not_found(test_client: TestClient, client):
    response = test_client.post(
        '/schedules',
        json={
            'date': '2023-09-15',
            'shift': 'morning',
            'description': 'A scheduled maintenance service',
            'client_id': client.id,
            'service_id': 999,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Service not found'}


def test_get_schedules_empty(test_client: TestClient):
    response = test_client.get('/schedules')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'schedules': []}


def test_get_schedules_with_schedules(
    test_client: TestClient, schedule, other_schedule
):
    schedule_schema = json.loads(
        SchedulePublic.model_validate(schedule).model_dump_json()
    )
    other_schedule_schema = json.loads(
        SchedulePublic.model_validate(other_schedule).model_dump_json()
    )

    response = test_client.get('/schedules')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'schedules': [schedule_schema, other_schedule_schema]
    }


def test_get_schedule_by_id(test_client: TestClient, schedule):
    schedule_schema = json.loads(
        (SchedulePublic.model_validate(schedule).model_dump_json())
    )

    response = test_client.get(f'/schedules/{schedule.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == schedule_schema


def test_get_not_found_schedule_by_id(test_client: TestClient, schedule):
    response = test_client.get(f'/schedules/{schedule.id + 1}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Schedule not found'}


def test_update_schedule(test_client: TestClient, schedule):
    response = test_client.put(
        f'/schedules/{schedule.id}',
        json={
            'date': '2023-09-16',
            'shift': 'afternoon',
            'description': 'Updated maintenance service',
            'client_id': schedule.client_id,
            'service_id': schedule.service_id,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': schedule.id,
        'date': '2023-09-16',
        'shift': 'afternoon',
        'description': 'Updated maintenance service',
        'client': {
            'id': schedule.client.id,
            'name': schedule.client.name,
        },
        'service': {
            'type': schedule.service.type,
        },
    }


def test_update_not_found_schedule(test_client: TestClient, schedule):
    response = test_client.put(
        f'/schedules/{schedule.id + 1}',
        json={
            'date': '2023-09-16',
            'shift': 'afternoon',
            'description': 'Updated maintenance service',
            'client_id': schedule.client_id,
            'service_id': schedule.service_id,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Schedule not found'}


def test_update_schedule_not_found_client(test_client: TestClient, schedule):
    response = test_client.put(
        f'/schedules/{schedule.id}',
        json={
            'date': '2023-09-16',
            'shift': 'afternoon',
            'description': 'Updated maintenance service',
            'client_id': 999,
            'service_id': schedule.service_id,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Client not found'}


def test_update_schedule_not_found_service(test_client: TestClient, schedule):
    response = test_client.put(
        f'/schedules/{schedule.id}',
        json={
            'date': '2023-09-16',
            'shift': 'afternoon',
            'description': 'Updated maintenance service',
            'client_id': schedule.client_id,
            'service_id': 999,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Service not found'}


def test_delete_schedule(test_client: TestClient, schedule):
    response = test_client.delete(f'/schedules/{schedule.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Schedule deleted'}


def test_delete_not_found_schedule(test_client: TestClient, schedule):
    response = test_client.delete(f'/schedules/{schedule.id + 1}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Schedule not found'}


def test_get_filtered_schedule_with_invalid_date(test_client: TestClient):
    response = test_client.get(
        '/schedules/filter',
        params={'start_date': '2024-11-05', 'end_date': '2024-10-28'},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'start_date must be <= than end_date'}
