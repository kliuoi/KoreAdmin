# from sqlalchemy.orm import Session
import pytest


# @pytest.mark.asyncio
def test_dept_add(client):
    response = client.post(
        "/system/v1/api/dept/add",
        json={"name": "test_dept"},
        # headers=superuser_token.headers,
        # cookies=superuser_token.cookies,
    )
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "test_dept"

    # 测试查询部门列表
    response = client.get(
        "/system/v1/api/dept/list",
        # headers=superuser_token.headers,
        # cookies=superuser_token.cookies,
    )
    assert response.status_code == 200
    assert any([dept["name"] == "test_dept" for dept in response.json()["data"]])

    # await db_session.rollback()
