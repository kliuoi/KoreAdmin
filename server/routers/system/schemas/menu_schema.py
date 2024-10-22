from pydantic import BaseModel


class MenuQueryListOut(BaseModel):
    """
    菜单列表-输出
    """

    id: int
    name: str
    type: str
    path: str | None
    method: str | None
    perms: str | None
    icon: str | None
    disabled: bool
    order: int

    children: list["MenuQueryListOut"]


class MenuQueryIn(BaseModel):
    """
    菜单查询-输入
    """

    id: int | None = None
    name: str | None = None


class MenuQueryOut(BaseModel):
    """
    菜单查询-输出
    """

    id: int
    name: str
    type: str
    path: str | None
    method: str | None
    perms: str | None
    icon: str | None
    disabled: bool
    order: int

    children: list[MenuQueryListOut]


class MenuCreateIn(BaseModel):
    """
    菜单创建-输入
    """

    name: str
    type: str
    path: str | None = None
    method: str | None = None
    perms: str | None = None
    icon: str | None = None
    disabled: bool = False
    order: int
    parent_id: int | None = None


class MenuCreateOut(BaseModel):
    """
    菜单创建-输出
    """

    id: int
    name: str
    type: str
    path: str | None
    method: str | None
    perms: str | None
    icon: str | None
    disabled: bool
    order: int


class MenuUpdateIn(BaseModel):
    """
    菜单更新-输入
    """

    id: int
    name: str
    type: str
    path: str | None = None
    method: str | None = None
    perms: str | None = None
    icon: str | None = None
    disabled: bool
    order: int


class MenuUpdateOut(BaseModel):
    """
    菜单更新-输出
    """

    id: int
    name: str
    type: str
    path: str | None
    method: str | None
    perms: str | None
    icon: str | None
    disabled: bool
    order: int


class MenuDeleteIn(BaseModel):
    """
    菜单删除-输入
    """

    id: int | None = None
    name: str | None = None
