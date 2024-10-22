from typing import List

from server.core.msd.service_base import Service_Base
from server.core.security.depends_auth import Auth
from server.core.response_base import errors
from server.db.db_casbin import get_casbin_enf

from .. import schemas
from .. import crud
from .. import models


class CasbinService(Service_Base):
    def __init__(self, auth: Auth):
        self.auth = auth
        self.enforcer = None

    async def get_enforcer(self):
        if not self.enforcer:
            self.enforcer = await get_casbin_enf()
        return self.enforcer

    async def get_roles_for_user(self, user_id: str) -> List[str]:
        """
        获取用户的所有角色
        """
        enforcer = await self.get_enforcer()
        return await enforcer.get_roles_for_user(user_id)

    async def delete_role_for_user(self, user_id: str, role: str) -> bool:
        """
        删除用户的指定角色
        """
        enforcer = await self.get_enforcer()
        return await enforcer.delete_role_for_user(user_id, role)

    async def add_role_for_user(self, user_id: str, role: str) -> bool:
        """
        为用户添加角色
        """
        enforcer = await self.get_enforcer()
        return await enforcer.add_role_for_user(user_id, role)

    async def get_permissions_for_user(self, user_id: str) -> List[List[str]]:
        """
        获取用户的所有权限
        """
        enforcer = await self.get_enforcer()
        return await enforcer.get_permissions_for_user(user_id)

    async def delete_policy(self, user_id: str, path: str, method: str) -> bool:
        """
        删除策略
        """
        enforcer = await self.get_enforcer()
        return await enforcer.remove_policy(user_id, path, method)

    async def add_permission_for_user(self, user_id: str, path: str, method: str) -> bool:
        """
        为用户添加权限
        """
        enforcer = await self.get_enforcer()
        return await enforcer.add_policy(user_id, path, method)

    async def reload_policy(self):
        """
        重新加载策略
        """
        enforcer = await self.get_enforcer()
        await enforcer.load_policy()

    async def has_permission(self, user_id: str, path: str, method: str) -> bool:
        """
        检查用户是否有特定权限
        """
        enforcer = await self.get_enforcer()
        return await enforcer.enforce(user_id, path, method)

    async def get_user_permissions(self, user_id: int):
        """
        获取用户的所有权限
        """
        try:
            return await self.get_permissions_for_user(str(user_id))
        except Exception as e:
            raise errors.ServerException(msg=f"获取用户权限失败: {str(e)}")

    async def get_role_permissions(self, role_id: int):
        """
        获取角色的所有权限
        """
        try:
            return await self.get_permissions_for_user(str(role_id))
        except Exception as e:
            raise errors.ServerException(msg=f"获取角色权限失败: {str(e)}")

    async def check_permission(self, user_id: int, path: str, method: str):
        """
        检查用户是否有特定权限
        """
        try:
            return await self.has_permission(str(user_id), path, method)
        except Exception as e:
            raise errors.ServerException(msg=f"检查权限失败: {str(e)}")
