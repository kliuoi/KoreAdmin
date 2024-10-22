from fastapi import APIRouter, Depends

from server.core.response_base import R, ResponseModel
from server.core.security.depends_auth import Auth, auth_support

from ... import services
from ... import schemas
from ... import crud


router = APIRouter()
api = APIRouter()


@api.get("/list/tree", summary="获取菜单树形结构")
async def get_menus(
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    return R.ok(
        msg="获取菜单树形结构成功",
        data=await crud.MenuCRUD(auth.db).menus_get_tree_list(v_schema=schemas.MenuQueryListOut),
    )


# 获取菜单详情
@api.post("/info", summary="获取菜单详情")
async def get_menu(
    obj: schemas.MenuQueryIn,
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    return R.ok(
        msg="获取菜单详情成功",
        data=await services.MenuService(auth).menu_get_info(obj=obj, v_schema=schemas.MenuQueryOut),
    )


# 创建菜单
@api.post("/add", summary="创建菜单")
async def create_menu(
    obj: schemas.MenuCreateIn,
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    return R.ok(
        msg="创建菜单成功",
        data=await services.MenuService(auth).menu_create(obj=obj, v_schema=schemas.MenuCreateOut),
    )


# 更新菜单
@api.put("/update", summary="更新菜单")
async def update_menu(
    obj: schemas.MenuUpdateIn,
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    return R.ok(
        msg="更新菜单成功",
        data=await services.MenuService(auth).menu_update(obj=obj, v_schema=schemas.MenuUpdateOut),
    )


# 删除菜单
@api.delete("/del", summary="删除菜单")
async def delete_menu(
    obj: schemas.MenuDeleteIn,
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    return R.ok(
        msg="删除菜单成功",
        data=await services.MenuService(auth).menu_delete(obj=obj),
    )
