from fastapi import APIRouter, Request, Depends

# from server.core.config import settings
from server.core.response_base import R

from server.core.security.depends_auth import Auth, auth_support
from server.db import get_casbin_enf

api = APIRouter()


@api.post("/testopen", summary="鉴权无权限测试")
async def auth_testopen(auth: Auth = Depends(auth_support.openauth)):
    if auth.user.email:
        return R.ok()


@api.post("/testadmin", summary="鉴权管理员测试")
async def auth_testadmin(auth: Auth = Depends(auth_support.admin_check)):
    return R.ok()


@api.post("/testuser", summary="鉴权用户测试")
async def auth_testuser(auth: Auth = Depends(auth_support)):
    return R.ok(auth.user.email)


@api.get("/{id}", summary="测试Casbin权限")
async def ltest1(request: Request, id: str):
    print(request.url)
    print(request.url.path)
    print(request.url.scheme)
    print(request.method)
    print(request.base_url)
    print(request.url.query)

    enf = await get_casbin_enf()
    # data = await enf.add_policy("testuser", request.url.path, request.method)
    data = await enf.add_policy("testuser", "*", request.method)
    data1 = enf.enforce("testuser", request.url.path, request.method)

    print(data)
    print(data1)
