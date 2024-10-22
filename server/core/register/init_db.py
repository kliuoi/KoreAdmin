from fastapi import FastAPI
from sqlalchemy import insert


from server.db import get_db_session, async_engine
from server.db.models import Base


def register_init_db(app: FastAPI):
    # 异步初始化数据库
    app.add_event_handler("startup", init_db_script().create_table)


class init_db_script:
    def __init__(self):
        self.datas = {}

    async def __generate_data(self, table_name: str, model):
        """
        生成数据

        :param table_name: 表名
        :param model: 数据表模型
        """
        async_session = get_db_session()
        db = await async_session.__anext__()
        datas = self.datas.get(table_name)
        await db.execute(insert(model), datas)
        await db.flush()
        await db.commit()
        print(f"{table_name} 表数据已生成")

    async def init_role(self):
        """
        初始化角色数据
        :return:
        """
        pass

    # 建立用户数据
    async def init_user(self):
        """
        初始化用户数据
        :return:
        """
        pass

    async def create_data(self):
        """
        创建数据表
        :return:
        """
        pass

    async def create_table(self):
        """
        创建数据表
        :return:
        """
        # 创建所有表
        from server.routers.system import models  # noqa: F401

        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
