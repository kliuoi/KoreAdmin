from fastapi import APIRouter

from .v1 import auth, user, role, menu, dept
# from .v1 import endpoint_test, casbin_api


v1_router = APIRouter()


v1_router.include_router(auth.router, prefix="/auth", tags=["鉴权模块-模板"])
v1_router.include_router(auth.api, prefix="/api/auth", tags=["鉴权模块-API"])

v1_router.include_router(user.router, prefix="/user", tags=["用户模块"])
v1_router.include_router(user.api, prefix="/api/user", tags=["用户模块-API"])

v1_router.include_router(role.router, prefix="/role", tags=["角色模块"])
v1_router.include_router(role.api, prefix="/api/role", tags=["角色模块-API"])

v1_router.include_router(menu.router, prefix="/menu", tags=["菜单模块"])
v1_router.include_router(menu.api, prefix="/api/menu", tags=["菜单模块-API"])

v1_router.include_router(dept.router, prefix="/dept", tags=["部门模块"])
v1_router.include_router(dept.api, prefix="/api/dept", tags=["部门模块-API"])

# v1_router.include_router(casbin_api.api, prefix="/api/casbin", tags=["Casbin模块-API"])

# v1_router.include_router(system_settings.router, prefix="/settings", tags=["系统设置"])
# v1_router.include_router(system_settings.api, prefix="/api/settings", tags=["系统设置-API"])

# v1_router.include_router(endpoint_test.api, prefix="/test", tags=["测试模块"])
