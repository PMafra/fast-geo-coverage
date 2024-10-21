import logging
from typing import Annotated

from fastapi import Depends, FastAPI

from app.configs.logging import setup_logging
from app.configs.settings import Settings, get_settings
from app.routers.v1 import router as v1_router

setup_logging()

app = FastAPI()
app.include_router(v1_router)

logger = logging.getLogger(__name__)


@app.get('/info')
async def info(settings: Annotated[Settings, Depends(get_settings)]):
	return {
		'app_name': settings.app_name,
		'admin_email': settings.admin_email,
		'items_per_user': settings.items_per_user,
	}


@app.get('/test-logging')
async def test_logging():
	logger.debug('This is a DEBUG message.')
	logger.info('This is an INFO message.')
	logger.warning('This is a WARNING message.')
	logger.error('This is an ERROR message.')
	logger.critical('This is a CRITICAL message.')
	return {'message': 'Logging test completed. Check your logs.'}
