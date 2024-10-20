import logging

from fastapi import APIRouter
from sqlmodel import select

from app.configs.database import (
	DbSessionDep,
)
from app.models.provider import (
	Provider,
)

logger = logging.getLogger(__name__)

router = APIRouter(
	prefix='/providers',
	tags=['providers'],
	responses={404: {'description': 'Not found'}},
)


@router.get('/providers')
async def read_providers(db: DbSessionDep):
	providers = db.exec(select(Provider)).all()
	return providers


@router.get('/test-logging')
async def test_logging():
	logger.debug('This is a DEBUG message.')
	logger.info('This is an INFO message.')
	logger.warning('This is a WARNING message.')
	logger.error('This is an ERROR message.')
	logger.critical('This is a CRITICAL message.')
	return {'message': 'Logging test completed. Check your logs.'}
