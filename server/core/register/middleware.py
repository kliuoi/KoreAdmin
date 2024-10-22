from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from server.core.config import settings


# 注册中间件
def register_middleware(app: FastAPI):
    """
    注册中间件
    :param app: FastAPI实例
    :return:
    """
    # 注册Session中间件, 用于存储Session
    app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET_KEY)
