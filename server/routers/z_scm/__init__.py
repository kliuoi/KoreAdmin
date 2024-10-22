from fastapi import APIRouter, FastAPI

from .views import v1_router

scm_router = APIRouter()

scm_router.include_router(v1_router, prefix="/v1")
