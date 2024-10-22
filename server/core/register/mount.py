from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from server.core.config import settings


# 注册挂载静态文件
def register_mount(app: FastAPI):
    """
    将静态文件目录注册到FastAPI应用中。
    :param app: FastAPI应用实例
    :return:
    """
    app.mount("/static", StaticFiles(directory=settings.FASTAPI_STATIC_FOLDER), name="static")
