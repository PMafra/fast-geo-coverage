from pydantic import EmailStr
from sqlmodel import SQLModel


class ProviderBase(SQLModel):
	name: str
	email: EmailStr
	phone_number: str
	language: str
	currency: str


class ProviderCreate(ProviderBase):
	pass


class ProviderRead(ProviderBase):
	id: int
