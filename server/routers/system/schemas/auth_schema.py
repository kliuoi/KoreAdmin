from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional
from .. import models


class Auth(BaseModel):
    db: AsyncSession
    token: str = None
    user: models.Sys_User = None

    class Config:
        # 接收任意类型
        arbitrary_types_allowed = True


class CustomOAuth2PasswordRequestForm:  # (OAuth2PasswordRequestForm):
    """
    自定义OAuth2PasswordRequestForm类, 增加验证码参数
    """

    def __init__(
        self,
        email: str = Form(),
        password: str = Form(),
        # captcha_key: Optional[str] = Form(default=""),
        # captcha: Optional[str] = Form(default=""),
    ):
        self.email = email
        self.password = password
        # self.captcha_key = captcha_key
        # self.captcha = captcha


# 用户登录模型
class UserLoginIn(BaseModel):
    """
    用户登录模型-输入
    """

    email: str = Field(..., description="邮箱", example="admin")
    password: str = Field(..., description="密码", example="admin")


class UserLoginOut(BaseModel):
    """
    用户登录模型-输出
    """

    access_token: str
    token_type: str


# 用户注册
class UserRegisterIn(BaseModel):
    """
    用户注册模型-输入
    """

    email: str = Field(..., description="邮箱", example="z")
    password: str = Field(..., description="密码", example="z")
    name: str | None = Field(None, description="姓名", example=None)


# 用户注册输出
class UserRegisterOut(BaseModel):
    """
    用户注册模型-输出
    """

    email: str = Field(..., description="邮箱")
    name: str | None = Field(None, description="姓名")
