from decimal import Decimal

from geoalchemy2.shape import to_shape
from pydantic import field_validator
from shapely.geometry import mapping, shape
from sqlmodel import SQLModel


class GeoJSON(SQLModel):
	type: str = 'Polygon'
	coordinates: list[list[list[float]]]

	@classmethod
	def from_geometry(cls, geom):
		return cls(**mapping(to_shape(geom)))

	def to_geometry(self):
		return shape(self.model_dump())


class ServiceAreaBase(SQLModel):
	name: str
	price: Decimal
	geojson: GeoJSON
	provider_id: int


class ServiceAreaCreate(ServiceAreaBase):
	@field_validator('geojson')
	def validate_geojson(cls, v):
		try:
			geom = v.to_geometry()
			if not geom.is_valid:
				raise ValueError('Invalid GeoJSON geometry')
			return v
		except Exception as e:
			raise ValueError(f'Invalid GeoJSON data: {e}') from e


class ServiceAreaRead(ServiceAreaBase):
	id: int
