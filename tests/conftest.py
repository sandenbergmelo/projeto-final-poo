import random

import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from projeto_final_poo.app import app
from projeto_final_poo.db.connection import get_session
from projeto_final_poo.db.models import (
    Address,
    Client,
    Schedule,
    Service,
    table_registry,
)


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    name = factory.Sequence(lambda n: f'test{n}')
    phone_number = factory.Faker('phone_number', locale='pt_BR')


class AddressFactory(factory.Factory):
    class Meta:
        model = Address

    street = factory.Faker('street_address')
    neighborhood = factory.Faker('street_name')
    reference = factory.Faker('secondary_address')
    number = factory.Faker('building_number')
    client_id = 1


class ServiceFactory(factory.Factory):
    class Meta:
        model = Service

    type = factory.Sequence(lambda n: f'service_type_{n}')
    description = factory.Faker('sentence', nb_words=4)
    price = factory.LazyAttribute(
        lambda _: round(random.uniform(10.00, 500.00), 2)
    )


class ScheduleFactory(factory.Factory):
    class Meta:
        model = Schedule

    date = factory.Faker('date_this_year')
    shift = factory.Faker(
        'random_element', elements=['morning', 'afternoon', 'evening']
    )
    description = factory.Faker('sentence', nb_words=6)
    client_id = 1
    service_id = 1


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def test_client(session):
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = lambda: session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def client(session: Session):
    client = ClientFactory()
    address = AddressFactory()
    client.address = address

    session.add(client)
    session.add(address)
    session.commit()
    session.refresh(client)

    return client


@pytest.fixture
def other_client(session: Session):
    client = ClientFactory()
    address = AddressFactory()
    client.address = address

    session.add(client)
    session.add(address)
    session.commit()
    session.refresh(client)

    return client


@pytest.fixture
def service(session: Session):
    service = ServiceFactory()

    session.add(service)
    session.commit()
    session.refresh(service)

    return service


@pytest.fixture
def other_service(session: Session):
    service = ServiceFactory()

    session.add(service)
    session.commit()
    session.refresh(service)

    return service


@pytest.fixture
def schedule(session: Session):
    schedule = ScheduleFactory()
    client = ClientFactory()
    service = ServiceFactory()

    schedule.client = client
    schedule.service = service

    session.add(schedule)
    session.commit()
    session.refresh(schedule)

    return schedule


@pytest.fixture
def other_schedule(session: Session):
    schedule = ScheduleFactory()
    client = ClientFactory()
    service = ServiceFactory()

    schedule.client = client
    schedule.service = service

    session.add(schedule)
    session.commit()
    session.refresh(schedule)

    return schedule
