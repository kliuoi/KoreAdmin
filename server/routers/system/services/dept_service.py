from typing import Any

from server.core.security.depends_auth import Auth
from server.core.response_base import errors
from server.core.msd.service_base import Service_Base
from server.core.security.passwd_encrypt import get_hash_password, verify_hash_password

from .. import schemas
from .. import crud
from .. import models


class DeptService(Service_Base):
    def __init__(self, auth: Auth):
        super().__init__(auth=auth)

    # 获取部门列表
    async def dept_get_list(
        self,
        *,
        v_schema: Any = None,
    ):
        """
        部门列表
        """
        db_depts = await crud.DeptCRUD(self.auth)._get_list()

        if db_depts is None:
            raise errors.RequestException(msg="部门列表为空")

        return await self.out_dict(obj=db_depts, v_schema=v_schema, v_return_list=True)

    async def dept_get_info(
        self,
        *,
        id: int = None,
        name: str = None,
        v_schema: Any = None,
    ):
        """
        查询部门是否存在

        :param id: 部门id
        :param name: 部门名称
        :param v_schema: 根据schema匹配数据
        :return: 部门存在: 返回部门数据库对象
        :return: 部门不存在: 返回False
        """

        db_dept = await crud.DeptCRUD(self.auth)._get(id=id, name=name)
        if db_dept is None:
            raise errors.RequestException(msg="部门不存在")

        return await self.out_dict(obj=db_dept, v_schema=v_schema)

    async def dept_create(
        self,
        *,
        obj: schemas.DeptCreateIn,
        v_schema: Any = None,
    ):
        """
        添加部门
        """
        # 查询部门是否存在
        db_dept = await crud.DeptCRUD(self.auth)._get(name=obj.name)
        if db_dept:
            raise errors.RequestException(msg="部门已存在")

        # 添加部门
        try:
            db_dept = await crud.DeptCRUD(self.auth)._create(obj=obj)
        except Exception:
            raise errors.RequestException(msg="部门添加失败")

        return await self.out_dict(obj=db_dept, v_schema=v_schema)

    async def dept_update(
        self,
        *,
        obj: schemas.DeptUpdateIn,
        v_schema: Any = None,
    ):
        """
        更新部门
        """
        # 查询部门是否存在
        db_dept = await crud.DeptCRUD(self.auth)._get(id=obj.id, name=obj.name)
        if db_dept is None:
            raise errors.RequestException(msg="部门不存在")

        # 更新部门
        try:
            db_dept = await crud.DeptCRUD(self.auth)._update(id=obj.id, obj_in=obj)
        except Exception:
            raise errors.RequestException(msg="部门更新失败")

        return await self.out_dict(obj=db_dept, v_schema=v_schema)

    async def dept_delete(
        self,
        *,
        obj: schemas.DeptDeleteIn,
    ):
        """
        删除部门
        """
        # 查询部门是否存在
        db_dept = await crud.DeptCRUD(self.auth)._get(id=obj.id, name=obj.name)
        if not db_dept:
            raise errors.RequestException(msg="部门不存在")

        try:
            await crud.DeptCRUD(self.auth)._delete(obj=obj)
        except Exception:
            raise errors.RequestException(msg="部门删除失败")
        else:
            return True
