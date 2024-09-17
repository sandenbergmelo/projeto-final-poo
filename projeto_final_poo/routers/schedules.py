from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from projeto_final_poo.custom_types.annotated_types import T_Session
from projeto_final_poo.db.models import Client, Schedule, Service
from projeto_final_poo.schemas.schemas import (
    Message,
    ScheduleCreate,
    ScheduleList,
    SchedulePublic,
    ScheduleQueryParams,
)

router = APIRouter(prefix='/schedules', tags=['schedules'])


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=SchedulePublic
)
def create_schedule(schedule: ScheduleCreate, session: T_Session):
    db_client = session.get(Client, schedule.client_id)
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Client not found'
        )

    db_service = session.get(Service, schedule.service_id)
    if not db_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Service not found'
        )

    db_schedule = Schedule(
        client_id=schedule.client_id,
        service_id=schedule.service_id,
        date=schedule.date,
        shift=schedule.shift,
        description=schedule.description,
    )

    db_schedule.client = db_client
    db_schedule.service = db_service

    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)

    return db_schedule


@router.get('/', response_model=ScheduleList)
def get_all_schedules(session: T_Session, limit: int = 10, offset: int = 0):
    schedules = session.scalars(
        select(Schedule).limit(limit).offset(offset)
    ).all()

    return {'schedules': schedules}


@router.get('/filter', response_model=ScheduleList)
def get_filtered_schedules(
    session: T_Session, params: ScheduleQueryParams = Depends()
):
    query = select(Schedule)

    if params.start_date:
        query = query.filter(Schedule.date >= params.start_date)

    if params.end_date:
        query = query.filter(Schedule.date <= params.end_date)

    if (
        params.end_date
        and params.end_date
        and params.start_date > params.end_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='start_date must be <= than end_date',
        )

    if params.client_id:
        query = query.filter(Schedule.client_id == params.client_id)

    if params.service_id:
        query = query.filter(Schedule.service_id == params.service_id)

    if params.shift:
        query = query.filter(Schedule.shift == params.shift)

    schedules = session.scalars(
        query.offset(params.offset).limit(params.limit)
    ).all()

    return {'schedules': schedules}


@router.get('/{id}', response_model=SchedulePublic)
def get_schedule_by_id(id: int, session: T_Session):
    schedule = session.get(Schedule, id)

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Schedule not found'
        )

    return schedule


@router.put('/{id}', response_model=SchedulePublic)
def update_schedule(id: int, schedule: ScheduleCreate, session: T_Session):
    db_schedule = session.get(Schedule, id)

    if not db_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Schedule not found'
        )

    db_client = session.get(Client, schedule.client_id)
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Client not found'
        )

    db_service = session.get(Service, schedule.service_id)
    if not db_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Service not found'
        )

    db_schedule.client_id = schedule.client_id
    db_schedule.service_id = schedule.service_id
    db_schedule.date = schedule.date
    db_schedule.shift = schedule.shift
    db_schedule.description = schedule.description

    session.commit()
    session.refresh(db_schedule)

    return db_schedule


@router.delete('/{id}', response_model=Message)
def delete_schedule(id: int, session: T_Session):
    db_schedule = session.get(Schedule, id)

    if not db_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Schedule not found'
        )

    session.delete(db_schedule)
    session.commit()

    return {'message': 'Schedule deleted'}
