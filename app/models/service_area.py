from decimal import Decimal
from hashlib import sha256
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry, WKTElement
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping, shape
from sqlmodel import (
	Column,
	Field,
	Index,
	Relationship,
	SQLModel,
	UniqueConstraint,
)

if TYPE_CHECKING:
	from app.models.provider import Provider


class ServiceArea(SQLModel, table=True):
	__tablename__: str = 'service_areas'

	id: int | None = Field(default=None, primary_key=True)
	name: str = Field(index=True)
	price: Decimal
	geojson: Geometry = Field(
		sa_column=Column(
			Geometry(geometry_type='POLYGON', srid=4326), nullable=False
		)
	)
	geojson_hash: str = Field(index=True)
	provider_id: int = Field(foreign_key='providers.id', nullable=False)
	provider: 'Provider' = Relationship(back_populates='service_areas')

	__table_args__ = (
		Index('ix_service_area_geojson', 'geojson', mysql_prefix='SPATIAL'),
		UniqueConstraint(
			'provider_id', 'geojson_hash', name='uq_provider_geojson'
		),
	)

	class Config:
		arbitrary_types_allowed = True

	def to_geojson(self):
		"""Convert the Geometry object to GeoJSON."""
		geom_shape = to_shape(self.geojson)
		return mapping(geom_shape)

	def set_geojson_hash(self):
		"""Set the hash of the GeoJSON data for uniqueness checking."""
		geojson_data = self.to_geojson()
		self.geojson_hash = sha256(
			str(geojson_data).encode('utf-8')
		).hexdigest()

	@classmethod
	def from_geojson(cls, name, price, geojson, provider_id):
		geometry = WKTElement(shape(geojson).wkt, srid=4326)

		instance = cls(
			name=name, price=price, geojson=geometry, provider_id=provider_id
		)
		instance.set_geojson_hash()
		return instance
