from sqlalchemy import select
from sqlalchemy.orm import Session

from projeto_final_poo.db.models import Client


def test_create_client(session: Session):
    client = Client(name='John Doe', phone_number='+5588999999999')

    session.add(client)
    session.commit()

    result = session.scalar(select(Client).where(Client.name == 'John Doe'))

    assert client.name == result.name
