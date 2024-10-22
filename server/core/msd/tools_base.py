from sqlalchemy import Row, RowMapping
from typing import Any, TypeVar
from asgiref.sync import sync_to_async
from datetime import datetime

RowData = Row | RowMapping | Any
R = TypeVar("R", bound=RowData)


# 封装增删改查工具类
class Tools_Base:

    async def out_dict(
        self,
        *,
        obj: Any,
        v_schema: Any | None = None,
        v_return_obj: bool = False,
        v_return_list: bool = False,
    ) -> dict:
        """
        返回数据格式化

        :param obj: 数据对象
        :param v_schema: 根据schema匹配数据
        :param v_return_obj: 是否直接返回对象
        :param v_return_list: 数据对象是否为列表
        :return:
        """

        if v_return_obj:
            return obj

        if v_schema:
            if v_return_list:
                obj_data = [v_schema.model_validate(await self.select_as_dict(item)).model_dump() for item in obj]
            else:
                obj_data = v_schema.model_validate(await self.select_as_dict(obj)).model_dump()
        else:
            if v_return_list:
                obj_data = [await self.select_as_dict(item) for item in obj]
            else:
                obj_data = await self.select_as_dict(obj)
        return obj_data

    @sync_to_async
    def select_as_dict(self, row: R) -> dict:
        """
        将row对象转换为字典

        :param row:
        :return:
        """
        obj_dict = row.__dict__
        if "_sa_instance_state" in obj_dict:
            del obj_dict["_sa_instance_state"]
            for key, value in obj_dict.items():
                # 如果是时间类型，则格式化为字符串
                if type(value) is datetime:
                    obj_dict[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        return obj_dict
