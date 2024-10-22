# 测试非管理员创建用户
def test_user_create_ordinary(client, ordinary_token, not_exist_token):
    response = client.post(
        "/system/v1/api/user/add",
        json={
            "email": not_exist_token.email,
            "password": not_exist_token.password,
        },
        headers=ordinary_token.headers,
        cookies=ordinary_token.cookies,
    )

    assert response.status_code == 401


def test_user_create(client, superuser_token, not_exist_token):
    """测试管理员创建用户"""
    response = client.post(
        "/system/v1/api/user/add",
        json={
            "email": not_exist_token.email,
            "password": not_exist_token.password,
        },
        headers=superuser_token.headers,
        cookies=superuser_token.cookies,
    )

    assert response.status_code == 200


def test_user_get_list(client, superuser_token):
    """测试管理员查看用户列表"""
    response = client.get(
        "/system/v1/api/user/list",
        headers=superuser_token.headers,
        cookies=superuser_token.cookies,
    )

    assert response.status_code == 200
    # 判断返回的数据是否包含普通用户
    assert any([user["email"] == superuser_token.email for user in response.json()["data"]])


# 测试普通用户查看用户列表
def test_user_get_list_ordinary(client, ordinary_token):
    response = client.get(
        "/system/v1/api/user/list",
        headers=ordinary_token.headers,
        cookies=ordinary_token.cookies,
    )

    assert response.status_code == 401


# 测试非管理员删除用户
def test_user_get_del_ordinary(client, ordinary_token, not_exist_token):
    response = client.request(
        method="DELETE",
        url="/system/v1/api/user/del",
        json={"email": not_exist_token.email},
        headers=ordinary_token.headers,
        cookies=ordinary_token.cookies,
    )

    assert response.status_code == 401


# 测试管理员删除非管理员用户
def test_user_get_del(client, superuser_token, ordinary_token):
    response = client.request(
        method="DELETE",
        url="/system/v1/api/user/del",
        json={"email": ordinary_token.email},
        headers=superuser_token.headers,
        cookies=superuser_token.cookies,
    )

    assert response.status_code == 200
