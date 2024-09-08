from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    message: str


class ClientSchema(BaseModel):
    name: str
    phone_number: str


class ClientPublic(BaseModel):
    id: int
    name: str
    phone_number: str
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


class ServiceList(BaseModel):
    services: list[ServicePublic]
