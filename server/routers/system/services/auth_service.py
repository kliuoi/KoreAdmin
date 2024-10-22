from fastapi import Response
from typing import Any
from datetime import datetime

from server.core.security.depends_auth import Auth, auth_support
from server.core.response_base import errors
from server.core.msd.service_base import Service_Base
from server.core.security.passwd_encrypt import get_hash_password, verify_hash_password
from server.core.security.jwt_utils import token_create_access
from server.core.security.depends_auth import auth_manager
from server.core.utils.timezone import timezone


from .. import models
from .. import schemas
from .. import crud


class AuthService(Service_Base):
    def __init__(self, auth: Auth):
        super().__init__(auth=auth)

    async def send_token(self, response: Response, user_identifier: str):
        access_token = await token_create_access(data=user_identifier)
        await auth_manager.set_cookie(response=response, token="bearer " + access_token)
        return access_token

    async def auth_login(
        self,
        response: Response,
        user: schemas.UserLoginIn,
    ) -> schemas.UserLoginOut:
        """
        用户登录
        """

        db_user: models.Sys_User = await crud.UserCRUD(self.auth)._get(email=user.email)

        # 判断用户是否存在以及解密密码并验证
        if db_user is None or not verify_hash_password(user.password, db_user.password):
            raise errors.RequestException(msg="用户或密码不正确")

        # 生成Token
        access_token = await self.send_token(response, db_user.uuid)
        # TODO 时间报错
        # await crud.UserCRUD(self.auth).update_login_time(db_user.email)

        return {"access_token": access_token, "token_type": "bearer"}
