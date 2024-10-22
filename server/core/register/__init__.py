from fastapi import FastAPI

from server.core.register.mount import register_mount
from server.core.register.exception_handlers import register_exception
from server.core.register.middleware import register_middleware
from server.core.register.cors import register_cors
from server.core.register.docs import register_docs
from server.core.register.init_db import register_init_db


def register_all(app: FastAPI):
    """
    注册所有内容，包含中间件、异常处理、挂载静态目录、初始化数据库
    """
    # 注册挂载静态文件
    register_mount(app)

    # 注册全局异常处理
    register_exception(app)

    # 注册中间件
    register_middleware(app)

    # 注册CORS
    register_cors(app)

    # 注册接口文档静态资源
    register_docs(app)
