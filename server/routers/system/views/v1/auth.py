from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from server.core.config import settings
from server.core.response_base import R, ResponseModel
from server.core.security.depends_auth import Auth, auth_support
from server.core.response_base.response_schema import StandardResponseCode
from server.core.response_base import errors


from ... import services
from ... import schemas


router = APIRouter()
api = APIRouter()


# 系统用户登录
@router.get("/login", summary="登录注册模板")
async def login_user(request: Request):
    return R.render("system/auth/index.json.jinja2", context={"request": request})


# 注册用户
@api.post("/register", summary="用户注册")
async def user_register(
    obj: schemas.UserRegisterIn,
    auth: Auth = Depends(auth_support.get_db),
) -> ResponseModel:
    if settings.FASTAPI_ALLOW_REGISTER:
        return R.error(code=StandardResponseCode.HTTP_500, msg="当前系统不允许注册")
    return R.ok(
        msg=f"用户{obj.email}注册成功",
        data=await services.UserService(auth).user_create(obj=obj, v_schema=schemas.UserRegisterOut),
    )


# Swagger UI专用
@api.post("/swagger_login", summary="Swagger登录")
async def swagger_login(
    response: Response,
    from_obj: OAuth2PasswordRequestForm = Depends(),
    auth: Auth = Depends(auth_support.get_db),
) -> schemas.UserLoginOut:
    # 把from_obj转换成UserLogin对象
    obj_user = schemas.UserLoginIn(email=from_obj.username, password=from_obj.password)

    return await services.AuthService(auth).auth_login(response, user=obj_user)


@api.post("/token", summary="获取登录Token")
async def token_get(
    response: Response,
    from_obj: schemas.UserLoginIn,
    auth: Auth = Depends(auth_support.get_db),
) -> schemas.UserLoginOut:
    return await services.AuthService(auth).auth_login(response, user=from_obj)


# 系统用户退出
@api.get("/logout", summary="系统用户退出")
async def logout(
    request: Request,
    response: Response,
):
    # 删除所有的cookies
    for cookie_name in request.cookies.keys():
        response.delete_cookie(key=cookie_name)
    return R.ok(msg="账号退出成功", data={"clear_access_token": "true"}, headers=response.headers)


# 刷新token
# TODO 修改send_token
# @api.post("/refresh", summary="刷新token")
# async def refresh_token(
#     response: Response,
#     auth: Auth = Depends(auth_support),
# ) -> ResponseModel:
#     access_token = await auth_support.send_token(response, auth.user.email)
#     return R.ok(
#         msg="刷新token成功", data={"access_token": access_token, "token_type": "bearer"}, headers=response.headers
#     )
