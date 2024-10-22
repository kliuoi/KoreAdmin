from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from server.core.security.depends_auth import Auth, auth_support
from server.core.config import settings
from server.core.response_base import errors, ResponseModel
from ...services.system_settings_service import SystemSettingsService

router = APIRouter()
api = APIRouter()


@api.get("/settings", response_model=ResponseModel[Dict[str, Any]])
async def get_system_settings(
    auth: Auth = Depends(auth_support),
):
    """
    获取当前系统设置
    """
    if not auth.user.is_admin:
        raise HTTPException(status_code=403, detail="只有管理员可以访问系统设置")

    service = SystemSettingsService(auth)
    settings_dict = await service.get_system_settings()
    return ResponseModel(data=settings_dict)


@api.put("/settings", response_model=ResponseModel[Dict[str, Any]])
async def update_system_settings(
    updated_settings: Dict[str, Any],
    auth: Auth = Depends(auth_support),
):
    """
    更新系统设置
    """
    if not auth.user.is_admin:
        raise HTTPException(status_code=403, detail="只有管理员可以修改系统设置")

    service = SystemSettingsService(auth)
    try:
        updated_settings_dict = await service.update_system_settings(updated_settings)
        return ResponseModel(data=updated_settings_dict, msg="系统设置更新成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.get("/env", response_model=ResponseModel[Dict[str, str]])
async def get_environment_variables(
    auth: Auth = Depends(auth_support),
):
    """
    获取当前环境变量
    """
    if not auth.user.is_admin:
        raise HTTPException(status_code=403, detail="只有管理员可以访问环境变量")

    service = SystemSettingsService(auth)
    env_vars = await service.get_environment_variables()
    return ResponseModel(data=env_vars)


@api.put("/env", response_model=ResponseModel[Dict[str, str]])
async def update_environment_variables(
    updated_env_vars: Dict[str, str],
    auth: Auth = Depends(auth_support),
):
    """
    更新环境变量
    """
    if not auth.user.is_admin:
        raise HTTPException(status_code=403, detail="只有管理员可以修改环境变量")

    service = SystemSettingsService(auth)
    try:
        updated_env_vars_dict = await service.update_environment_variables(updated_env_vars)
        return ResponseModel(data=updated_env_vars_dict, msg="环境变量更新成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
