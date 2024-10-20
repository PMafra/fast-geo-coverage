from sqlmodel import (
	Field,
	SQLModel,
)


class Provider(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	name: str = Field(index=True)
	email: str = Field(index=True)
	phone_number: str = Field(index=True)
	language: str
	currency: str
