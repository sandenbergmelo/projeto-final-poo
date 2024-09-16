import json

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from projeto_final_poo.db.models import ShiftEnum
from projeto_final_poo.schemas.schemas import SchedulePublic
from tests.conftest import ScheduleFactory


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


def test_get_filtered_schedule_client_service_id(
    test_client: TestClient,
    session: Session,
    client,
    service,
):
    expected_schedules = 5

    session.bulk_save_objects(
        ScheduleFactory.create_batch(
            5,
            client_id=client.id,
            service_id=service.id,
        )
    )

    session.bulk_save_objects(
        ScheduleFactory.create_batch(3, client_id=999, service_id=999)
    )

    session.commit()

    response = test_client.get(
        '/schedules/filter',
        params={'client_id': client.id, 'service_id': service.id},
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['schedules']) == expected_schedules


def test_get_filtered_schedule_shift(
    test_client: TestClient,
    session: Session,
    client,
    service,
):
    expected_schedules = 5
    schedule_shift = ShiftEnum.AFTERNOON

    session.bulk_save_objects(
        ScheduleFactory.create_batch(
            5, client_id=client.id, service_id=service.id, shift=schedule_shift
        )
    )
    session.bulk_save_objects(
        ScheduleFactory.create_batch(
            5,
            client_id=client.id,
            service_id=service.id,
            shift=ShiftEnum.EVENING,
        )
    )
    session.commit()

    response = test_client.get(
        '/schedules/filter',
        params={'shift': schedule_shift.value},
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['schedules']) == expected_schedules
