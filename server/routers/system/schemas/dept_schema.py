from pydantic import BaseModel, Field


# 部门列表
class DeptQueryListOut(BaseModel):
    id: int
    name: str
    level: int | None
    sort: int | None
    disabled: bool


class DeptQueryIn(BaseModel):
    id: int | None = None
    name: str | None = None
    disabled: bool | None = False


class DeptQueryOut(BaseModel):
    id: int
    name: str
    level: int
    sort: int
    disabled: bool


class DeptCreateIn(BaseModel):
    name: str
    sort: int | None = Field(None, description="排序")
    level: int | None = Field(None, description="部门层级")
    disabled: bool | None = Field(False, description="是否禁用")


class DeptCreateOut(BaseModel):
    id: int
    name: str
    level: int | None
    sort: int | None
    disabled: bool | None


class DeptUpdateIn(BaseModel):

    id: int
    name: str
    level: int
    sort: int | None
    disabled: bool | None = False


class DeptUpdateOut(BaseModel):
    id: int
    name: str
    level: int
    sort: int
    disabled: bool


class DeptDeleteIn(BaseModel):
    id: int
    name: str
