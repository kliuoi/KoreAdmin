# 测试fastapi文档
def test_openapi_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_docs(client):
    response = client.get("/redoc")
    assert response.status_code == 200
