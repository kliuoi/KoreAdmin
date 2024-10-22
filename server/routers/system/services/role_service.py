from typing import Any

from server.core.security.depends_auth import Auth
from server.core.response_base import errors
from server.core.msd.service_base import Service_Base
from server.core.security.passwd_encrypt import get_hash_password, verify_hash_password

from .. import schemas
from .. import crud
from .. import models


class RoleService(Service_Base):
    def __init__(self, auth: Auth):
        super().__init__(auth=auth)

    async def role_get_list(
        self,
        *,
        v_schema: Any = None,
    ):
        """
        获取角色列表
        """

        db_data = await crud.RoleCRUD(self.auth)._get_list()
        if not db_data:
            raise errors.RequestException(msg="角色列表为空")

        return await self.out_dict(obj=db_data, v_schema=v_schema, v_return_list=True)

    async def role_get_info(
        self,
        *,
        id: int = None,
        name: str = None,
        v_schema: Any = None,
    ):
        """
        获取角色信息
        """
        db_role = await crud.RoleCRUD(self.auth)._get(id=id, name=name)
        if db_role is None:
            raise errors.RequestException(msg="角色不存在")

        return await self.out_dict(obj=db_role, v_schema=v_schema)

    async def role_create(
        self,
        *,
        obj: schemas.RoleCreateIn,
        v_schema: Any = None,
    ):
        """
        创建角色
        """

        db_role = await crud.RoleCRUD(self.auth)._get(name=obj.name)
        if db_role:
            raise errors.RequestException(msg="角色已存在")

        try:
            db_role = await crud.RoleCRUD(self.auth)._create(obj=obj)
        except Exception:
            raise errors.RequestException(msg="创建角色失败")

        return await self.out_dict(obj=db_role, v_schema=v_schema)

    async def role_update(
        self,
        *,
        obj: schemas.RoleUpdateIn,
        v_schema: Any = None,
    ):
        """
        更新角色信息
        """

        db_role = await crud.RoleCRUD(self.auth)._get(name=obj.name)
        if db_role is None:
            raise errors.RequestException(msg="角色不存在")
        # 校验角色名称是否重复
        db_role = await crud.RoleCRUD(self.auth)._get(name=obj.name)

        try:
            await crud.RoleCRUD(self.auth)._update(id=obj.id, obj_in=obj)
        except Exception:
            raise errors.RequestException(msg="更新角色失败")

        return await self.out_dict(obj=db_role, v_schema=v_schema)

    async def role_update_permission(
        self,
        *,
        obj: schemas.RoleUpdatePermissionIn,
    ):
        """
        角色更新权限
        """
        try:
            # 获取角色当前的所有权限
            current_permissions = await self.get_permissions_for_user(str(obj.role_id))

            # 删除所有现有权限
            for perm in current_permissions:
                await self.delete_policy(str(obj.role_id), perm[0], perm[1])

            # 添加新的权限
            for perm in obj.permissions:
                await self.add_permission_for_user(str(obj.role_id), perm.path, perm.method)

            # 重新加载策略
            await self.reload_policy()

            return True
        except Exception as e:
            raise errors.ServerException(msg=f"更新角色权限失败: {str(e)}")

    async def role_delete(
        self,
        *,
        obj: schemas.RoleDeleteIn,
    ) -> bool:
        """
        删除角色
        """
        db_role = await crud.RoleCRUD(self.auth)._get(id=obj.id, name=obj.name)
        if db_role is None:
            raise errors.RequestException(msg="角色不存在")
        try:
            await crud.RoleCRUD(self.auth)._delete(id=obj.id)
        except Exception:
            raise errors.RequestException(msg="删除角色失败")

        return True
