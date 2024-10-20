from fastapi import APIRouter

from app.routers.v1.providers import (
	router as providers_router,
)

router = APIRouter(prefix='/v1')
router.include_router(providers_router)
