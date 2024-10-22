from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import Row, RowMapping, and_, select, update, delete
from typing import Any, TypeVar
from pydantic import BaseModel

from server.db.models import MappedBase
from server.core.response_base import errors
from server.core.security.depends_auth import Auth

from .tools_base import Tools_Base


# 泛型
ModelType = TypeVar("ModelType", bound=MappedBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUB_Base(Tools_Base):
    def __init__(
        self,
        auth: Auth,
        model: ModelType = None,
    ):
        self.auth = auth
        self.db = auth.db
        self.model = model

    async def _get(
        self,
        join: list[Any] | None = None,
        **kwargs,
    ) -> Any:
        """
        通过传参获取一条数据, 支持关联查询

        :param join: 可选, 需要关联查询的模型列表里的字段, 例如: join=[models.Sys_User.depts, models.Sys_User.roles]
        :param kwargs: 查询条件, 支持关联查询条件, 例如: id(字段名)="admin@example.com"(字段值)
        :return: 查询结果
        """
        # 查询条件如果为空, 抛出异常
        if not kwargs:
            raise errors.RequestException(msg="查询参数至少有一个, 不能为空")

        # 动态构建查询条件
        conditions = [getattr(self.model, key) == value for key, value in kwargs.items()]

        # 构建基础查询
        query = select(self.model)

        # 添加关联查询
        if join:
            for relation in join:
                query = query.options(joinedload(relation))

        # 添加查询条件
        query = query.where(and_(*conditions))

        # 执行查询
        result = await self.db.execute(query)
        db_data = result.unique().scalar_one_or_none()

        return db_data

    async def _get_list(
        self,
        model: Any | None = None,
        **kwargs,
    ) -> Any:
        """
        获取数据列表, 支持动态筛选条件
        示例

        :param model: 可选, 指定要查询的模型, 如果为None则使用self.model
        :param kwargs: 动态筛选条件, 格式为 model.field=value
        :return: 查询结果列表
        """
        # 如果没有指定模型, 使用默认的self.model
        if model is None:
            model = self.model

        # 创建基础查询
        query = select(model)

        # 用于存储所有筛选条件
        filter_conditions = []

        # 遍历所有传入的筛选条件
        for key, value in kwargs.items():
            if "." in key:
                # 处理关联模型的筛选条件, 例如 user.role.name="admin"
                attr_name, field_name = key.split(".", 1)
                if hasattr(model, attr_name):
                    attr = getattr(model, attr_name)
                    if hasattr(attr.property.mapper.class_, field_name):
                        if isinstance(value, (list, tuple)):
                            # 如果值是列表或元组, 使用 in_ 操作符
                            filter_conditions.append(getattr(attr.property.mapper.class_, field_name).in_(value))
                        else:
                            # 否则使用等于操作符
                            filter_conditions.append(getattr(attr.property.mapper.class_, field_name) == value)
            elif hasattr(model, key):
                # 处理当前模型的筛选条件
                if isinstance(value, (list, tuple)):
                    # 如果值是列表或元组, 使用 in_ 操作符
                    filter_conditions.append(getattr(model, key).in_(value))
                else:
                    # 否则使用等于操作符
                    filter_conditions.append(getattr(model, key) == value)

        # 如果有筛选条件, 将它们添加到查询中
        if filter_conditions:
            query = query.where(and_(*filter_conditions))

        # 执行查询
        result = await self.db.execute(query)
        # 获取所有结果
        db_data = result.scalars().all()

        return db_data

    async def _create(
        self,
        *,
        obj: CreateSchemaType,
    ) -> Any:
        """
        创建一条数据

        :param obj: 创建数据的schema
        :return:
        """
        obj_data = self.model(**obj.model_dump())
        self.db.add(obj_data)
        await self.db.flush()
        await self.db.refresh(obj_data)

        return obj_data

    async def _update(
        self,
        *,
        id: int,
        obj_in: UpdateSchemaType | dict,
    ) -> Any:
        """
        更新一条数据

        :param id: 要更新的记录的ID
        :param obj_in: 更新数据的schema或字典
        :return: 更新后的数据
        """
        # 如果obj_in是BaseModel的子类, 则调用model_dump()
        if isinstance(obj_in, BaseModel):
            update_data = obj_in.model_dump(exclude_unset=True)
        elif isinstance(obj_in, dict):
            update_data = obj_in
        else:
            raise errors.ServerException(msg="obj_in 必须是 Pydantic 模型或字典类型")

        db_data = await self.db.execute(update(self.model).where(self.model.id == id).values(**update_data))
        await self.db.flush()

        db_data = await self._get(id=id)
        await self.db.refresh(db_data)

        return db_data

    async def _delete(
        self,
        *,
        id: int,
    ) -> int:
        """
        通过主键id删除一条数据

        :param id: 主键id
        :return:
        """
        result = await self.db.execute(delete(self.model).where(self.model.id == id))
        await self.db.flush()
        return result.rowcount
