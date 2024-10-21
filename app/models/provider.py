from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
	from app.models.service_area import ServiceArea


class Provider(SQLModel, table=True):
	__tablename__: str = 'providers'

	id: int | None = Field(default=None, primary_key=True)
	name: str = Field(index=True)
	email: str = Field(index=True)
	phone_number: str = Field(index=True)
	language: str
	currency: str
	service_areas: list['ServiceArea'] = Relationship(
		back_populates='provider'
	)
