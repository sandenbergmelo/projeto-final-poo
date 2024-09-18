from fastapi import APIRouter, HTTPException, status

from projeto_final_poo.custom_types.annotated_types import T_Session
from projeto_final_poo.db.models import Address, Client
from projeto_final_poo.schemas.schemas import (
    AddressesList,
    AddressPublic,
    AddressSchema,
    AddressUpdate,
)

router = APIRouter(prefix='/address', tags=['address'])


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=AddressPublic
)
def add_address(address: AddressSchema, session: T_Session):
    db_client = session.get(Client, address.client_id)

    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Client not found',
        )

    db_address = Address(
        client_id=address.client_id,
        street=address.street,
        neighborhood=address.neighborhood,
        reference=address.reference,
        number=address.number,
    )

    session.add(db_address)
    session.commit()

    session.refresh(db_address)
    session.refresh(db_client)

    return db_address


@router.get('/{client_id}', response_model=AddressesList)
def get_addresses_by_client(client_id: int, session: T_Session):
    db_client = session.get(Client, client_id)

    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Client not found',
        )

    return {'addresses': db_client.addresses}


@router.put('/{id}', response_model=AddressPublic)
def update_address(id: int, address: AddressUpdate, session: T_Session):
    db_address = session.get(Address, id)

    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Address not found',
        )

    db_address.street = address.street
    db_address.neighborhood = address.neighborhood
    db_address.reference = address.reference
    db_address.number = address.number

    session.commit()
    session.refresh(db_address)

    return db_address


@router.delete('/{id}', response_model=dict)
def delete_address(id: int, session: T_Session):
    db_address = session.get(Address, id)

    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Address not found',
        )

    db_client = session.get(Client, db_address.client_id)

    if db_address and len(db_client.addresses) <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="It is not possible to delete the client's only address.",
        )

    session.delete(db_address)
    session.commit()

    return {'message': 'Address deleted'}
