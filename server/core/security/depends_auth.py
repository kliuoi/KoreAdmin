from fastapi import Request, Response, Depends
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from sqlalchemy.ext.asyncio import AsyncSession
from casbin import AsyncEnforcer
from sqlalchemy import select
from typing import Any, cast

from server.core.config import settings
from server.db import get_db_session, get_casbin_enf
from server.core.response_base import errors
from server.core.security.jwt_utils import token_decode_access
from server.routers.system import models
from server.routers.system.schemas import Auth


class AuthManager(OAuth2):
    def __init__(
        self,
        token_url: str = settings.SWAGGER_LOGIN_URL,
        authorization_mode: str = settings.AUTHORIZATION_MODE,
        authorization_name: str = settings.AUTHORIZATION_NAME,
    ):
        # 获取Token的URL
        self.token_url = token_url
        # 认证模式
        self.authorization_mode = authorization_mode
        # 鉴权使用名称
        self.authorization_name = authorization_name
        self.auto_error = False

        flows = OAuthFlowsModel(password=cast(Any, {"tokenUrl": self.token_url}))
        super().__init__(
            flows=flows,
            auto_error=self.auto_error,
        )

    # 设置Cookie
    async def set_cookie(self, *, response: Response, token: str):
        if self.authorization_mode == "cookie":
            response.set_cookie(key=self.authorization_name, value=token, httponly=True)

    # 删除Cookie
    async def del_cookie(self, response: Response):
        if self.authorization_mode == "cookie":
            response.delete_cookie(key=self.authorization_name)

    async def _get_token(
        self,
        request: Request,
    ):
        authorization: str = None

        if self.authorization_mode == "header":
            authorization: str = request.headers.get(self.authorization_name)
        elif self.authorization_mode == "cookie":
            authorization: str = request.cookies.get(self.authorization_name)
        else:
            raise errors.ServerException(msg="未设置认证模式")

        if not authorization:
            raise errors.ReLoginException(msg="用户未登录, 未读取到Token")

        scheme, token = get_authorization_scheme_param(authorization)

        if scheme.lower() != "bearer":
            raise errors.TokenException(msg="Token格式错误, 需要Bearer Token")

        return token

    async def _validate_token(
        self,
        response: Response,
        token: str,
    ):
        # 验证Token
        try:
            payload = await token_decode_access(token)
            user_identifier: str = payload.get("sub")
        except Exception:
            # 删除Cookie
            await self.del_cookie(response)
            raise errors.TokenException(msg="用户Token解密失败, 可能是Token已过期", headers=response.headers)

        return user_identifier

    async def _validate_user(
        self,
        response: Response,
        user_identifier: str,
        db: AsyncSession,
    ):
        # 验证用户信息
        result = await db.execute(select(models.Sys_User).where(models.Sys_User.uuid == user_identifier))
        db_user = result.scalars().first()
        if not db_user.is_active:
            # 删除Cookie
            await self.del_cookie(response)
            raise errors.AuthenticationException(msg="用户不存在或未在激活状态", headers=response.headers)

        return db_user

    async def __call__(
        self,
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_db_session),
    ):
        token = await self._get_token(request)
        user_identifier = await self._validate_token(response, token)
        db_user = await self._validate_user(response, user_identifier, db)

        return Auth(db=db, token=token, user=db_user)


auth_manager = AuthManager()


class Auth_Support:

    # 只返回db
    async def get_db(
        self,
        db: AsyncSession = Depends(get_db_session),
    ) -> Auth:
        return Auth(db=db)

    async def openauth(
        self,
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_db_session),
    ) -> Auth:
        try:
            token, db_user = await auth_manager(request=request, response=response, db=db)
        except Exception as e:
            # 如果是ReLoginException异常，直接抛出, 一般是签名过期或者Token错误
            if e.__class__.__name__ == "TokenException" or e.__class__.__name__ == "AuthenticationException":
                raise e
            else:
                return Auth(db=db)
        return Auth(db=db, token=token, user=db_user)

    # 需要用户登录
    async def __call__(
        request: Request,
        response: Response,
        auth: str = Depends(auth_manager),
        db: AsyncSession = Depends(get_db_session),
    ) -> Auth:

        return auth

    async def admin_check(
        self,
        request: Request,
        response: Response,
        auth: Auth = Depends(__call__),
        db: AsyncSession = Depends(get_db_session),
    ) -> Auth:

        if not auth.user.is_admin:
            raise errors.PermissionException(msg="无权限访问, 需要管理员权限")
        return auth

    async def permission_check(
        self,
        request: Request,
        permission: str = None,
        auth: Auth = Depends(__call__),
        enforce: AsyncEnforcer = Depends(get_casbin_enf),
    ) -> Auth:

        if settings.PERMISSION_MODE == "casbin":
            if not enforce.enforce(auth.user.uuid, request.url.path, request.method):
                raise errors.PermissionException(msg=f"无权限访问, 需要权限: {permission}")
        elif settings.PERMISSION_MODE == "role-menu":
            if not permission:
                raise errors.ServerException(msg="接口未设置权限标识")
        else:
            raise errors.ServerException(msg="未设置鉴权模式")

        return auth


auth_support = Auth_Support()
