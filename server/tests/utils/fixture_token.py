from starlette.testclient import TestClient
from pydantic import BaseModel

from server.core.config import settings


# TODO: 增加过期的签名token
class SecurityToken(BaseModel):
    email: str
    password: str
    headers: dict[str, str] = {}
    cookies: dict[str, str] = {}


def get_authentication_token(client: TestClient, email: str, password: str) -> dict[str, str]:
    if email == "not" and password == "not":
        return SecurityToken(email=email, password=password)
    data = {
        "email": email,
        "password": password,
    }
    response = client.post("/system/v1/api/auth/token", data=data)
    try:
        response.raise_for_status()
        token_type = response.json()["token_type"]
        access_token = response.json()["access_token"]
        headers = {settings.AUTHORIZATION_NAME: f"{token_type} {access_token}"}
        cookies = {settings.AUTHORIZATION_NAME: f"{token_type} {access_token}"}
    except Exception:
        return SecurityToken(email=email, password=password)

    return SecurityToken(email=email, password=password, headers=headers, cookies=cookies)
