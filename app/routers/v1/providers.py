import logging

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.configs.database import DbSessionDep
from app.models.provider import Provider
from app.routers.schemas.provider import ProviderCreate, ProviderRead

logger = logging.getLogger(__name__)

router = APIRouter(
	prefix='/providers',
	tags=['providers'],
	responses={404: {'description': 'Not found'}},
)


@router.get('/', response_model=list[ProviderRead])
async def read_providers(db: DbSessionDep):
	providers = db.exec(select(Provider)).all()
	return providers


@router.post('/', response_model=ProviderRead)
async def create_provider(provider: ProviderCreate, db: DbSessionDep):
	provider = Provider.model_validate(provider)
	db.add(provider)
	db.commit()
	db.refresh(provider)
	return provider


@router.get('/{provider_id}', response_model=ProviderRead)
async def read_provider(provider_id: int, db: DbSessionDep):
	provider = db.get(Provider, provider_id)
	if not provider:
		raise HTTPException(status_code=404, detail='Provider not found')
	return provider


@router.delete('/{provider_id}', status_code=204)
def delete_hero(provider_id: int, db: DbSessionDep):
	provider = db.get(Provider, provider_id)
	if not provider:
		raise HTTPException(status_code=404, detail='Provider not found')
	db.delete(provider)
	db.commit()
