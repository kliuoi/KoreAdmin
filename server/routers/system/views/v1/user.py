from fastapi import APIRouter, Depends

from server.core.response_base import R, ResponseModel
from server.core.security.depends_auth import Auth, auth_support

from ... import schemas
from ... import services


router = APIRouter()
api = APIRouter()


@api.get("/list", summary="获取用户列表")
async def user_get_list(
    auth: Auth = Depends(auth_support.admin_check),
) -> ResponseModel:
    return R.ok(
        msg="查询成功",
        data=await services.UserService(auth).user_get_list(v_schema=schemas.UserQueryOut),
    )


@api.post("/info/current", summary="获取当前用户详情")
async def user_current_info(
    auth: Auth = Depends(auth_support),
) -> ResponseModel:
    return R.ok(
        msg="查询成功",
        data=await services.UserService(auth).user_get_info(id=auth.user.id, v_schema=schemas.UserQueryOut),
    )


@api.post("/info", summary="指定用户详情")
async def user_get_info(
    obj: schemas.UserQueryIn,
    auth: Auth = Depends(auth_support.admin_check),
) -> ResponseModel:
    return R.ok(
        msg="查询成功",
        data=await services.UserService(auth).user_get_info(id=obj.id, v_schema=schemas.UserQueryOut),
    )


@api.post("/add", summary="用户新建")
async def user_create(
    obj: schemas.UserCreateIn,
    auth: Auth = Depends(auth_support.admin_check),
) -> ResponseModel:
    return R.ok(
        msg=f"用户{obj.email}创建成功",
        data=await services.UserService(auth).user_create(obj=obj, v_schema=schemas.UserQueryOut),
    )


@api.put("/update/info", summary="用户更新")
async def user_update(
    obj: schemas.UserUpdateIn,
    auth: Auth = Depends(auth_support),
) -> ResponseModel:
    if not auth.user.is_admin:
        if obj.id != auth.user.id:
            return R.error(msg="无权限修改其他用户")
    return R.ok(
        msg=f"用户{obj.email}更新成功",
        data=await services.UserService(auth).user_update(id=obj.id, obj=obj, v_schema=schemas.UserQueryOut),
    )


@api.put("/update/dept", summary="用户更新部门")
async def user_update_dept(
    obj: schemas.UserUpdateDeptIn,
    auth: Auth = Depends(auth_support.admin_check),
) -> ResponseModel:
    return R.ok(
        msg="更新部门成功",
        data=await services.UserService(auth).user_update_dept(obj),
    )


@api.put("/update/role", summary="用户更新角色")
async def user_update_role(
    obj: schemas.UserUpdateRoleIn,
    auth: Auth = Depends(auth_support.admin_check),
) -> ResponseModel:
    return R.ok(
        msg="更新角色成功",
        data=await services.UserService(auth).user_update_role(obj),
    )


@api.put("/resetpwd", summary="用户重置密码")
async def user_resetpwd(
    obj: schemas.UserUpdatePasswordIn,
    auth: Auth = Depends(auth_support.admin_check),
) -> ResponseModel:
    if not auth.user.is_admin:
        if auth.user.id != obj.id:
            return R.error(msg="无权限修改")
    return R.ok(
        msg=f"用户{obj.email}修改密码成功",
        data=await services.UserService(auth).user_resetpwd(obj),
    )


@api.delete("/del", summary="用户删除")
async def user_delete(
    obj: schemas.UserDeleteIn,
    auth: Auth = Depends(auth_support.admin_check),
) -> ResponseModel:
    return R.ok(
        msg="用户删除成功",
        data=await services.UserService(auth).user_delete(id=obj.id, email=obj.email),
    )
