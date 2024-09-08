import random

import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from projeto_final_poo.app import app
from projeto_final_poo.db.connection import get_session
from projeto_final_poo.db.models import Client, Service, table_registry


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    name = factory.Sequence(lambda n: f'test{n}')
    phone_number = factory.Faker('phone_number', locale='pt_BR')


class ServiceFactory(factory.Factory):
    class Meta:
        model = Service

    type = factory.Sequence(lambda n: f'service_type_{n}')
    description = factory.Faker('sentence', nb_words=4)
    price = factory.LazyAttribute(
        lambda _: round(random.uniform(10.00, 500.00), 2)
    )


# @pytest.fixture(scope='session')
# def engine():
#     _engine = create_engine(
#         'sqlite:///:memory:',
#         connect_args={'check_same_thread': False},
#     )
#     return _engine


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
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def client(session: Session):
    client = ClientFactory()

    session.add(client)
    session.commit()
    session.refresh(client)

    return client


@pytest.fixture
def other_client(session: Session):
    client = ClientFactory()

    session.add(client)
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
