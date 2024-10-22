from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator, Any

from server.core.config import settings


# 创建异步数据库引擎
async_engine = create_async_engine(
    settings.DB_ASYNC_URL,
    **settings.DB_PARAMS[settings.DB_DRIVER],
)


# 异步会话工厂
AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


# 用于为路由提供数据库会话的函数
async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    """
    获取数据库会话

    :return: AsyncSession
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
