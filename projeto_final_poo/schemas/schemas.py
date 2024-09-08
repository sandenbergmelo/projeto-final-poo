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
