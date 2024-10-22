from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from server.core.config import settings
from server.core.register import register_all
from server.core.register.init_db import init_db_script
from server.routers import register_router


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    启动初始化

    :return:
    """
    # 创建数据库表
    await init_db_script().create_table()

    yield


def create_app() -> FastAPI:
    app = FastAPI(
        **settings.get_fastapi_params(),
        lifespan=register_init,
    )

    # 注册所有内容，包含中间件、异常处理、挂载静态目录等
    register_all(app)

    # 导入路由
    register_router(app)

    return app


def initdb_common():
    """
    初始化数据库，包括创建数据库、表结构等。
    """
    # 初始化数据库
    asyncio.run(init_db_script().create_table())
