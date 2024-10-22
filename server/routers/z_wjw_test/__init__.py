from fastapi import FastAPI, APIRouter

from .views import get_class

wjw_test_router = APIRouter()

wjw_test_router.include_router(get_class.api, prefix="/auth", tags=["测试模块-获取班级"])
