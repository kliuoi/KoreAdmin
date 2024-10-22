from starlette.testclient import TestClient
import pytest

from server.tests.utils.fixture_token import SecurityToken, get_authentication_token


# 写两个账户及密码，一个管理员账户，一个普通账户，让测试用例可以使用
@pytest.fixture(scope="session")
def superuser_token(client: TestClient) -> SecurityToken:
    """
    管理员admin用户测试
    :param client:
    :return:
    """
    return get_authentication_token(client=client, email="admin", password="adminadmin")


@pytest.fixture(scope="session")
def ordinary_token(client: TestClient) -> SecurityToken:
    """
    普通用户
    :param client:
    :return:
    """
    return get_authentication_token(client=client, email="test", password="test")


@pytest.fixture(scope="session")
def not_exist_token(client: TestClient) -> SecurityToken:
    """
    不存在的用户
    :param client:
    :return:
    """
    return get_authentication_token(client=client, email="not", password="not")
