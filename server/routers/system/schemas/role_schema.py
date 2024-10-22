from pydantic import BaseModel
from typing import List


class RoleQueryListIn(BaseModel):
    """
    角色列表查询-输入
    """

    id: int | None = None
    name: str | None = None
    enable: bool | None = True


class RoleQueryListOut(BaseModel):
    """
    角色列表-输出
    """

    id: int
    name: str
    enable: bool
    description: str | None = None


class RoleQueryIn(BaseModel):
    """
    角色详情查询-输入
    """

    id: int | None = None


class RoleQueryOut(BaseModel):
    """
    指定角色查询-输出
    """

    id: int
    name: str
    enable: bool
    description: str | None = None


class RoleCreateIn(BaseModel):
    """
    角色创建-输入
    """

    name: str
    enable: bool
    description: str | None = None


class RoleCreateOut(BaseModel):
    """
    角色创建-输出
    """

    name: str
    enable: bool
    description: str | None = None


class RoleUpdateIn(BaseModel):
    """
    角色更新-输入
    """

    id: int
    name: str
    enable: bool
    description: str | None = None


class RoleUpdateOut(BaseModel):
    """
    角色更新-输出
    """

    id: int
    name: str
    enable: bool
    description: str | None = None


class RolePermissionIn(BaseModel):
    """
    权限模型
    """

    path: str
    method: str


class RoleUpdatePermissionIn(BaseModel):
    """
    角色更新权限模型
    """

    role_id: int
    permissions: List[RolePermissionIn]


class RoleDeleteIn(BaseModel):
    """
    角色删除-输入
    """

    id: int | None = None
    name: str | None = None
