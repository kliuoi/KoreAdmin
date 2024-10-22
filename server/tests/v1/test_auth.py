import pytest

from server.core.config import settings
from server.routers.system import crud
from server.core.security.jwt_utils import token_create_access


def test_register_repeat(client, not_exist_token):
    """测试注册以及重复注册"""
    response = client.post(
        "/system/v1/api/auth/register",
        json={"email": not_exist_token.email, "password": not_exist_token.password},
    )
    assert response.status_code == 200
    assert response.json()["msg"] == f"用户{not_exist_token.email}注册成功"

    response = client.post(
        "/system/v1/api/auth/register",
        json={"email": not_exist_token.email, "password": not_exist_token.password},
    )
    assert response.json()["msg"] == "用户已存在"


# 测试禁止注册
def test_register_forbidden(client, not_exist_token):
    settings.FASTAPI_ALLOW_REGISTER = True
    response = client.post(
        "/system/v1/api/auth/register",
        json={"email": not_exist_token.email, "password": not_exist_token.password},
    )
    assert response.status_code == 500
    assert response.json()["msg"] == "当前系统不允许注册"
    settings.FASTAPI_ALLOW_REGISTER = False


# 测试登录
@pytest.mark.asyncio
async def test_login(client, db_session, not_exist_token):
    """
    测试登录
    """
    # crud.UserCRUD(db_session).user_create(
    #     obj={
    #         "email": not_exist_token.email,
    #         "password": not_exist_token.password,
    #     }
    # )

    response = client.post(
        "/system/v1/api/auth/token",
        data={"email": not_exist_token.email, "password": not_exist_token.password},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] == await token_create_access(not_exist_token.email)


# 测试登录失败
def test_login_fail(client, ordinary_token):
    """
    测试登录失败
    """
    # 用户名错误
    response = client.post(
        "/system/v1/api/auth/token",
        data={"email": ordinary_token.email + "1", "password": ordinary_token.password},
    )
    assert response.status_code == 400
    assert response.json()["msg"] == "用户或密码不正确"

    # 密码错误
    response = client.post(
        "/system/v1/api/auth/token",
        data={"email": ordinary_token.email, "password": ordinary_token.password + "1"},
    )
    assert response.status_code == 400
    assert response.json()["msg"] == "用户或密码不正确"
