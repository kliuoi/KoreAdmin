from fastapi import APIRouter, Depends

from server.core.response_base import R, ResponseModel
from server.core.security.depends_auth import Auth, auth_support

from ... import services
from ... import schemas
from ... import crud


router = APIRouter()
api = APIRouter()


@api.get("/list", summary="获取部门列表")
async def dept_list(
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    return R.ok(
        msg="获取成功",
        data=await services.DeptService(auth).dept_get_list(v_schema=schemas.DeptQueryListOut),
    )


@api.post("/info", summary="获取部门详情")
async def dept_get(
    obj: schemas.DeptQueryIn,
    auth: Auth = Depends(auth_support.openauth),
) -> ResponseModel:
    return R.ok(
        msg="获取成功",
        data=await services.DeptService(auth).dept_get_info(id=obj.id, name=obj.name, v_schema=schemas.DeptQueryOut),
    )


@api.post("/add", summary="添加部门")
async def dept_add(
    obj: schemas.DeptCreateIn,
    auth: Auth = Depends(auth_support.get_db),
) -> ResponseModel:
    return R.ok(
        msg="添加成功",
        data=await services.DeptService(auth).dept_create(obj=obj, v_schema=schemas.DeptCreateOut),
    )


@api.put("/update", summary="更新部门")
async def dept_update(
    obj: schemas.DeptUpdateIn,
    auth: Auth = Depends(auth_support),
) -> ResponseModel:
    return R.ok(
        msg="更新成功",
        data=await services.DeptService(auth).dept_update(obj=obj, v_schema=schemas.DeptUpdateOut),
    )


@api.delete("/delete", summary="删除部门")
async def dept_delete(
    obj: schemas.DeptDeleteIn,
    auth: Auth = Depends(auth_support),
) -> ResponseModel:
    return R.ok(
        msg="删除成功",
        data=await services.DeptService(auth).dept_delete(obj=obj),
    )
