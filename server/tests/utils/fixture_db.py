from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import asyncio


from server.db import async_engine
from typing import AsyncGenerator, Any
from server.db import AsyncSessionLocal

TestingAsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


# 创建异步数据库引擎
# async_engine = create_async_engine("sqlite+aiosqlite:///")


async def create_table():
    from server.routers.system import models  # noqa: F401, E402
    from server.db.models import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create_table())


async def get_test_db_session() -> AsyncGenerator[AsyncSession, Any]:
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
