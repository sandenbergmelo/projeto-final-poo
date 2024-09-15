from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from projeto_final_poo.custom_types.annotated_types import T_Session
from projeto_final_poo.db.models import Address, Client
from projeto_final_poo.schemas.schemas import (
    ClientList,
    ClientPublic,
    ClientSchema,
    Message,
)

router = APIRouter(prefix='/clients', tags=['clients'])


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=ClientPublic
)
def create_client(client: ClientSchema, session: T_Session):
    db_client = session.scalar(
        select(Client).where(Client.phone_number == client.phone_number)
    )

    if db_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Phone number already exists in another client',
        )

    db_client = Client(name=client.name, phone_number=client.phone_number)

    db_address = Address(
        street=client.street,
        neighborhood=client.neighborhood,
        reference=client.reference,
        number=client.number,
        client_id=db_client.id,
    )

    db_client.address = db_address

    session.add(db_client)
    session.add(db_address)
    session.commit()

    session.refresh(db_client)

    return db_client


@router.get('/', response_model=ClientList)
def get_all_clients(session: T_Session, limit: int = 10, offset: int = 0):
    clients = session.scalars(select(Client).limit(limit).offset(offset))
    return {'clients': clients}


@router.get('/{id}', response_model=ClientPublic)
def get_client_by_id(id: int, session: T_Session):
    client = session.get(Client, id)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Client not found'
        )

    return client


@router.put('/{id}', response_model=ClientPublic)
def update_client(id: int, client: ClientSchema, session: T_Session):
    db_client = session.get(Client, id)

    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Client not found'
        )

    client_with_same_phone_number = session.scalar(
        select(Client).where(Client.phone_number == client.phone_number)
    )

    if (
        client_with_same_phone_number
        and id != client_with_same_phone_number.id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Phone number already exists in another client',
        )

    if not db_client.phone_number == client.phone_number:
        db_client.phone_number = client.phone_number

    db_client.name = client.name
    db_client.address.street = client.street
    db_client.address.neighborhood = client.neighborhood
    db_client.address.reference = client.reference
    db_client.address.number = client.number

    session.commit()
    session.refresh(db_client)

    return db_client


@router.delete('/{id}', response_model=Message)
def delete_client(id: int, session: T_Session):
    db_client = session.get(Client, id)

    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Client not found'
        )

    session.delete(db_client.address)
    session.delete(db_client)
    session.commit()

    return {'message': 'Client deleted'}
