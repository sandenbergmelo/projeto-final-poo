from fastapi import APIRouter, status
from sqlalchemy import select

from projeto_final_poo.custom_types.annotated_types import T_Session
from projeto_final_poo.db.models import Service
from projeto_final_poo.helpers.exceptions import NotFoundException
from projeto_final_poo.schemas.schemas import (
    Message,
    ServiceList,
    ServicePublic,
    ServiceSchema,
)

router = APIRouter(prefix='/services', tags=['services'])


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=ServicePublic
)
def create_service(service: ServiceSchema, session: T_Session):
    db_service = Service(
        type=service.type,
        description=service.description,
        price=service.price,
    )

    session.add(db_service)
    session.commit()

    session.refresh(db_service)

    return db_service


@router.get('/', response_model=ServiceList)
def get_all_services(session: T_Session, limit: int = 10, offset: int = 0):
    services = session.scalars(select(Service).limit(limit).offset(offset))
    return {'services': services}


@router.get('/{id}', response_model=ServicePublic)
def get_service_by_id(id: int, session: T_Session):
    service = session.get(Service, id)

    if not service:
        raise NotFoundException('Service not found')

    return service


@router.put('/{id}', response_model=ServicePublic)
def update_service(id: int, service: ServiceSchema, session: T_Session):
    db_service = session.get(Service, id)

    if not db_service:
        raise NotFoundException('Service not found')

    db_service.type = service.type
    db_service.description = service.description
    db_service.price = service.price

    session.commit()
    session.refresh(db_service)

    return db_service


@router.delete('/{id}', response_model=Message)
def delete_service(id: int, session: T_Session):
    db_service = session.get(Service, id)

    if not db_service:
        raise NotFoundException('Service not found')

    session.delete(db_service)
    session.commit()

    return {'message': 'Service deleted'}
