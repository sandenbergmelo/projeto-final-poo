import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from projeto_final_poo.db.models import ShiftEnum


class Message(BaseModel):
    message: str


class AddressSchema(BaseModel):
    street: str
    neighborhood: str
    reference: str
    number: str

    model_config = ConfigDict(from_attributes=True)


class ClientSchema(BaseModel):
    name: str
    phone_number: str
    street: str
    neighborhood: str
    reference: str
    number: str


class ClientPublic(BaseModel):
    id: int
    name: str
    phone_number: str
    address: AddressSchema

    model_config = ConfigDict(from_attributes=True)


class ClientList(BaseModel):
    clients: list[ClientPublic]


class ServiceSchema(BaseModel):
    type: str
    description: str
    price: float


class ServicePublic(BaseModel):
    id: int
    type: str
    description: str
    price: float

    model_config = ConfigDict(from_attributes=True)


class ScheduleClient(BaseModel):
    id: int
    name: str


class ScheduleService(BaseModel):
    type: str


class ServiceList(BaseModel):
    services: list[ServicePublic]


class ScheduleCreate(BaseModel):
    client_id: int = Field(ge=1, description='Client ID must be at least 1')
    service_id: int = Field(ge=1, description='Service ID must be at least 1')
    date: datetime.date
    shift: ShiftEnum = Field(
        ..., description="Shift must be 'morning', 'afternoon', or 'evening'"
    )
    description: str


class SchedulePublic(BaseModel):
    id: int
    date: datetime.date
    shift: ShiftEnum
    description: str
    client: ScheduleClient
    service: ScheduleService


class ScheduleList(BaseModel):
    schedules: list[SchedulePublic]


class ScheduleQueryParams(BaseModel):
    client_id: Optional[int] = Field(
        None, ge=1, description='ID of the client. Must be at least 1.'
    )
    service_id: Optional[int] = Field(
        None, ge=1, description='ID of the service. Must be at least 1.'
    )
    start_date: Optional[datetime.date] = Field(
        None,
        description='Start date of the schedule range. Format: YYYY-MM-DD.',
    )
    end_date: Optional[datetime.date] = Field(
        None, description='End date of the schedule range. Format: YYYY-MM-DD.'
    )
    shift: Optional[ShiftEnum] = Field(
        None, description='Shift of the schedule.'
    )
    offset: Optional[int] = Field(None, description='Number of items to skip.')
    limit: Optional[int] = Field(
        None, description='Number of items to return.'
    )

    @model_validator(mode='before')
    def check_date_range(cls, values):
        start_date = values.get('start_date')
        end_date = values.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValueError(
                'End date must be greater than or equal to start date.'
            )

        return values
