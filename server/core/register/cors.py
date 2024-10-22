from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from server.core.config import settings


def register_cors(app: FastAPI):
    """ """
    # 跨域配置
    if settings.CORS_ORIGIN_ENABLE:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ALLOW_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS,
        )
