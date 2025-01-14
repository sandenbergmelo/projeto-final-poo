import random
from datetime import timedelta
from pathlib import Path

import alembic
import alembic.command
from alembic.config import Config
from rich import print
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from projeto_final_poo.helpers.factories import (
    ClientFactory,
    ScheduleFactory,
    ServiceFactory,
)
from projeto_final_poo.helpers.settings import env

alembic_config = Config(
    Path(__file__).parent.parent.parent.parent / 'alembic.ini'
)

engine = create_engine(env.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


def reset_db():
    db_file = Path(__file__).absolute().parent.parent.parent / 'database.db'

    try:
        print('[bold yellow]Cleaning database...[/]')
        if db_file.is_file():
            db_file.unlink()

        alembic.command.downgrade(alembic_config, 'base')
        alembic.command.upgrade(alembic_config, 'head')
        print('[bold green]Database cleaned![/]')

    except Exception as e:
        print(e)


def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def seed_data():
    print('\n[bold yellow]Seeding database...[/]')

    services = ServiceFactory.create_batch(10)
    session.add_all(services)
    session.commit()

    clients = ClientFactory.create_batch(10)
    session.add_all(clients)
    session.commit()

    addresses = ClientFactory.create_batch(10)
    session.add_all(addresses)
    session.commit()

    schedules = ScheduleFactory.create_batch(10)
    session.add_all(schedules)
    session.commit()

    print('[bold green]Database seeded![/]')


if __name__ == '__main__':
    reset_db()
    seed_data()
