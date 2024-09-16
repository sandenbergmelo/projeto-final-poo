import random
from datetime import datetime, timedelta
from os import system
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from projeto_final_poo.db.models import (
    Address,
    Client,
    Schedule,
    Service,
)
from projeto_final_poo.helpers.settings import env
from projeto_final_poo.schemas.schemas import ShiftEnum

engine = create_engine(env.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


def reset_db():
    db_file = Path(__file__).absolute().parent.parent.parent / 'database.db'

    if db_file.is_file():
        db_file.unlink()

    try:
        system('alembic upgrade head')
        print('Database cleaned')
    except Exception as e:
        print(e)


def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def seed_data():
    reset_db()
    services = [
        Service(type='Cleaning', description='Office cleaning', price=50.00),
        Service(
            type='Maintenance',
            description='Building maintenance',
            price=150.00,
        ),
        Service(
            type='Consulting', description='Business consulting', price=200.00
        ),
        Service(
            type='IT Support',
            description='Technical support for IT issues',
            price=100.00,
        ),
        Service(
            type='Security', description='Security services', price=300.00
        ),
        Service(
            type='Gardening', description='Garden maintenance', price=80.00
        ),
        Service(
            type='Catering',
            description='Event catering services',
            price=250.00,
        ),
        Service(type='Legal', description='Legal consulting', price=500.00),
        Service(
            type='Marketing', description='Marketing strategies', price=400.00
        ),
        Service(
            type='Training',
            description='Employee training sessions',
            price=150.00,
        ),
    ]

    session.add_all(services)
    session.commit()

    # Criação de clientes e endereços
    clients = [
        Client(name=f'Client {i}', phone_number=f'123-456-78{i:02d}')
        for i in range(1, 11)
    ]

    session.add_all(clients)
    session.commit()

    addresses = [
        Address(
            street=f'{i * 100} Elm St',
            neighborhood='Neighborhood {i%3}',
            reference=f'Reference {i}',
            number=f'{i * 10}',
            client_id=i,
        )
        for i in range(1, 11)
    ]

    session.add_all(addresses)
    session.commit()

    today = datetime.now().date()
    end_date = today + timedelta(days=60)

    schedules = [
        Schedule(
            client_id=(i % 10) + 1,
            service_id=(i % 10) + 1,
            date=random_date(today, end_date),
            description=f'description {(i % 10) + 1}',
            shift=ShiftEnum.MORNING.value
            if i % 3 == 0
            else ShiftEnum.AFTERNOON.value
            if i % 3 == 1
            else ShiftEnum.EVENING.value,
        )
        for i in range(1, 11)
    ]

    session.add_all(schedules)
    session.commit()

    print('Database seeded successfully!')


if __name__ == '__main__':
    seed_data()
