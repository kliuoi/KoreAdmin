from fastapi import APIRouter

from .views import v1_router


system_router = APIRouter()

system_router.include_router(v1_router, prefix="/v1")
