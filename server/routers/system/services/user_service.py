from typing import Any

from server.core.config import settings
from server.core.security.depends_auth import Auth
from server.core.response_base import errors
from server.core.msd.service_base import Service_Base
from server.core.security.passwd_encrypt import get_hash_password, verify_hash_password

from .. import models
from .. import schemas
from .. import crud


class UserService(Service_Base):
    def __init__(self, auth: Auth):
        super().__init__(auth=auth)

    async def user_get_list(
        self,
        *,
        v_schema: Any = None,
    ):
        """
        获取用户列表

        :param v_schema: 根据schema匹配数据
        :return:
        """
        db_users = await crud.UserCRUD(self.auth)._get_list()
        if not db_users:
            raise errors.RequestException(msg="用户列表为空")

        return await self.out_dict(obj=db_users, v_schema=v_schema, v_return_list=True)

    async def user_get_info(
        self,
        *,
        id: int,
        v_schema: Any = None,
    ):
        """
        获取用户信息

        :param id: 用户id
        :return:
        """

        db_user = await crud.UserCRUD(self.auth)._get(id=id)

        if db_user is None:
            raise errors.RequestException(msg="用户不存在")

        return await self.out_dict(obj=db_user, v_schema=v_schema)

    async def user_create(
        self,
        *,
        obj: schemas.UserCreateIn,
        v_schema: Any = None,
    ):
        """
        创建一个用户

        :param user:
        :return:
        """
        db_user = await crud.UserCRUD(self.auth)._get(email=obj.email)
        if db_user:
            raise errors.RequestException(msg="用户名已存在")
        obj.password = get_hash_password(obj.password)
        try:
            db_user = await crud.UserCRUD(self.auth)._create(obj=obj)
        except Exception:
            raise errors.RequestException(msg="建立用户失败")

        return await self.out_dict(obj=db_user, v_schema=v_schema)

    async def user_update(
        self,
        *,
        id: int,
        obj: schemas.UserUpdateIn,
        v_schema: Any = None,
    ):
        """
        更新用户信息

        :param user:
        :return:
        """

        db_user = await crud.UserCRUD(self.auth)._get(id=id)
        if db_user is None:
            raise errors.RequestException(msg="用户不存在")
        if obj.email != db_user.email:
            if await crud.UserCRUD(self.auth)._get(email=obj.email):
                raise errors.RequestException(msg="用户名已存在")
        # TODO 校验其他数据是否合法
        # TODO 关于校验，最好还是放到schemas里面，这样更加规范
        try:
            db_user = await crud.UserCRUD(self.auth)._update(id=id, obj_in=obj)
        except Exception:
            raise errors.RequestException(msg="更新用户失败")

        return await self.out_dict(obj=db_user, v_schema=v_schema)

    async def user_update_dept(self, obj: schemas.UserUpdateDeptIn):
        """
        用户更新部门
        """
        try:
            # 检查用户是否存在
            user: models.Sys_User = await crud.UserCRUD(self.auth)._get(join=[models.Sys_User.depts], id=obj.user_id)
            if user is None:
                raise errors.RequestException(msg="用户不存在")

            if user.depts:
                user.depts.clear()

            for dept_id in obj.dept_ids:
                dept = await crud.DeptCRUD(self.auth)._get(id=dept_id)
                if not dept:
                    raise errors.RequestException(msg=f"部门ID: {dept_id}不存在")
                user.depts.add(dept)

            await self.auth.db.flush()

            return True
        except Exception as e:
            raise errors.RequestException(msg=f"更新用户部门失败: {str(e)}")

    async def user_update_role(self, obj: schemas.UserUpdateRoleIn):
        """
        用户更新角色
        """
        try:
            # 检查用户是否存在
            user: models.Sys_User = await crud.UserCRUD(self.auth)._get(join=[models.Sys_User.roles], id=obj.user_id)
            if not user:
                raise errors.RequestException(msg="用户不存在")

            if user.roles:
                user.roles.clear()

            for role_id in obj.role_ids:
                role = await crud.RoleCRUD(self.auth)._get(id=role_id)
                if not role:
                    raise errors.RequestException(msg=f"角色 ID {role_id} 不存在")
                user.roles.add(role)

            await self.auth.db.flush()

            return True
        except Exception as e:
            raise errors.RequestException(msg=f"更新用户角色失败: {str(e)}")

    async def user_resetpwd(
        self,
        *,
        obj: schemas.UserUpdatePasswordIn,
    ) -> bool:
        """
        重置密码
        :param obj:
        :return:
        """
        db_user: models.Sys_User = await crud.UserCRUD(self.auth)._get(id=obj.id)
        if db_user is None:
            raise errors.RequestException(msg="用户不存在")
        if obj.password == obj.new_password:
            raise errors.RequestException(msg="新密码不能与原密码相同")
        if not verify_hash_password(obj.password, db_user.password):
            raise errors.RequestException(msg="密码错误")

        try:
            db_user.password = get_hash_password(obj.new_password)
            self.db.flush()
        except Exception:
            raise errors.RequestException(msg="重置密码失败")
        return True

    async def user_delete(
        self,
        *,
        id: int = None,
        email: str = None,
    ) -> bool:
        """
        删除用户

        :param id: 用户id
        :param email: 用户名
        :return:
        """
        if id:
            db_user = await crud.UserCRUD(self.auth)._get(id=id)
        elif email:
            db_user = await crud.UserCRUD(self.auth)._get(email=email)

        if db_user is None:
            raise errors.RequestException(msg="用户不存在")
        try:
            await crud.UserCRUD(self.auth)._delete(id=db_user.id)
        except Exception:
            raise errors.RequestException(msg="删除用户失败")

        return True
