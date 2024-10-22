from fastapi import APIRouter, Depends

from server.core.response_base import R, ResponseModel
from server.core.security.depends_auth import Auth, auth_support


from ... import schemas
from ... import services
from ... import crud


router = APIRouter()
api = APIRouter()


@api.get("/list", summary="获取角色列表")
async def role_list(
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    return R.ok(
        msg="获取成功",
        data=await services.RoleService(auth).role_get_list(v_schema=schemas.RoleQueryListOut),
    )


@api.post("/info", summary="指定角色详情")
async def role_info(
    obj: schemas.RoleQueryIn,
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    return R.ok(
        msg="获取成功",
        data=await services.RoleService(auth).role_get_info(id=obj.id, v_schema=schemas.RoleQueryOut),
    )


@api.post("/add", summary="角色建立")
async def role_create(
    obj: schemas.RoleCreateIn,
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    return R.ok(
        msg="角色建立成功",
        data=await services.RoleService(auth).role_create(obj=obj, v_schema=schemas.RoleCreateOut),
    )


@api.put("/update", summary="角色信息更新")
async def role_update(
    obj: schemas.RoleUpdateIn,
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    return R.ok(
        msg="角色信息更新成功",
        data=await services.RoleService(auth).role_update(obj=obj, v_schema=schemas.RoleUpdateOut),
    )


@api.put("/update/permission", summary="角色更新权限")
async def role_update_permission(
    obj: schemas.RoleUpdatePermissionIn,
    auth: Auth = Depends(auth_support.admin_check),
) -> ResponseModel:
    return R.ok(
        msg="更新权限成功",
        data=await services.RoleService(auth).role_update_permission(obj=obj),
    )


@api.delete("/del", summary="角色删除")
async def role_delete(
    obj: schemas.RoleDeleteIn,
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    R.ok(
        msg="角色删除成功",
        data=await services.RoleService(auth).role_delete(obj=obj),
    )
