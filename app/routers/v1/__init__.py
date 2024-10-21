from fastapi import APIRouter

from app.routers.v1.providers import router as providers_router
from app.routers.v1.service_areas import router as service_area_router

router = APIRouter(prefix='/v1')
router.include_router(providers_router)
router.include_router(service_area_router)
