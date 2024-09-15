from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Client:
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    phone_number: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    address: Mapped['Address'] = relationship(
        'Address',
        uselist=False,
        init=False,
    )


@table_registry.mapped_as_dataclass
class Address:
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    street: Mapped[str]
    neighborhood: Mapped[str]
    reference: Mapped[str]
    number: Mapped[str]

    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


@table_registry.mapped_as_dataclass
class Service:
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    type: Mapped[str]
    description: Mapped[str]
    price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
