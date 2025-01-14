import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from projeto_final_poo.app import app
from projeto_final_poo.db.connection import get_session
from projeto_final_poo.db.models import (
    table_registry,
)
from projeto_final_poo.helpers.factories import (
    AddressFactory,
    ClientFactory,
    ScheduleFactory,
    ServiceFactory,
)


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
