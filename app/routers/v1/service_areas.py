import logging

from fastapi import APIRouter
from sqlmodel import select

from app.configs.database import DbSessionDep
from app.models.service_area import ServiceArea
from app.routers.schemas.service_area import ServiceAreaCreate, ServiceAreaRead

logger = logging.getLogger(__name__)

router = APIRouter(
	prefix='/service-areas',
	tags=[
		'service-areas',
	],
	responses={404: {'description': 'Not found'}},
)


@router.get('/', response_model=list[ServiceAreaRead])
async def read_service_areas(db: DbSessionDep):
	providers = db.exec(select(ServiceArea)).all()
	return providers


@router.post('/', status_code=201)
async def create_service_area(
	service_area: ServiceAreaCreate, db: DbSessionDep
):
	geometry = service_area.geojson.to_geometry()
	service_area_instance = ServiceArea.from_geojson(
		name=service_area.name,
		price=service_area.price,
		geojson=geometry,
		provider_id=service_area.provider_id,
	)

	db.add(service_area_instance)
	db.commit()
	db.refresh(service_area_instance)
