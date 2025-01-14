import sys

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session

from projeto_final_poo.helpers.settings import env


def _get_engine():  # pragma: no cover
    try:
        return create_engine(env.DATABASE_URL)
    except OperationalError as e:
        print(f'Operational error creating the database engine: {e}')
        sys.exit(1)
    except SQLAlchemyError as e:
        print(f'General error creating the database engine: {e}')
        sys.exit(1)


def get_session():  # pragma: no cover
    try:
        engine = _get_engine()
        with Session(engine) as session:
            yield session
    except IntegrityError as e:
        print(f'Database integrity error: {e}')
        sys.exit(1)
    except OperationalError as e:
        print(f'Operational error accessing the database: {e}')
        sys.exit(1)
    except SQLAlchemyError as e:
        print(f'General error accessing the database: {e}')
        sys.exit(1)
