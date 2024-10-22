from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, update

from server.core.msd.crub_base import CRUB_Base
from server.core.security.depends_auth import Auth
from server.core.response_base import errors
from server.core.security.passwd_encrypt import get_hash_password, verify_hash_password
from server.core.utils.timezone import timezone

from .. import models


class UserCRUD(CRUB_Base):
    """
    用户增删改查
    """

    def __init__(self, auth: Auth):
        super().__init__(
            auth=auth,
            model=models.Sys_User,
        )

    # async def user_get(
    #     self,
    #     *,
    #     id: int = None,
    #     username: str = None,
    # ):
    #     """
    #     查看用户是否存在

    #     :param id: 用户id
    #     :param username: 用户名
    #     :return: 用户存在: 返回用户数据库对象
    #     :return: 用户不存在: 返回False
    #     """
    #     se = select(models.Sys_User)
    #     where_list = []
    #     if id:
    #         where_list.append(models.Sys_User.id == id)
    #     if username:
    #         where_list.append(models.Sys_User.username == username)
    #     if where_list:
    #         se = se.where(and_(*where_list))
    #     else:
    #         raise errors.RequestException(msg="查询参数至少有一个, 不能为空")

    #     result = await self.db.execute(se)
    #     db_user = result.scalars().first()

    #     if db_user is None:
    #         return None
    #     return db_user

    async def update_last_login(self, id: int):
        obj = await self._update(id, obj_in={"last_login": timezone.now()})
        return obj

    async def update_login_time(self, email: str) -> int:
        """
        更新用户登录时间

        :param db:
        :param email:
        :return:
        """
        user = await self.db.execute(
            update(self.model).where(self.model.email == email).values(last_login_time=timezone.now())
        )
        return user.rowcount
