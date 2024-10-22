from pydantic import BaseModel, Field


class UserQueryOut(BaseModel):
    """
    用户模型-输出
    """

    id: int
    email: str
    name: str | None = None
    is_active: bool = True
    is_admin: bool = False
    remark: str | None = None


class UserQueryIn(BaseModel):
    """
    用户模型-查询
    """

    id: int
    # email: str | None = None


class UserCreateIn(BaseModel):
    """
    用户建立模型-输入
    """

    email: str = Field(..., description="用户名", example="z")
    password: str = Field(..., description="密码", example="z")
    name: str | None = Field(None, description="姓名", example=None)


class UserUpdateIn(BaseModel):
    """
    用户更新模型-输入
    """

    id: int
    email: str | None = None
    name: str | None = None
    is_active: bool = True
    is_admin: bool = False
    remark: str | None = None


class UserUpdatePasswordIn(BaseModel):
    """
    用户修改密码模型-输入
    """

    id: int
    email: str
    password: str
    new_password: str


class UserUpdateDeptIn(BaseModel):
    """
    用户更新部门模型
    """

    user_id: int
    dept_ids: list[int] | None = []


class UserUpdateRoleIn(BaseModel):
    """
    用户更新角色模型
    """

    user_id: int
    role_ids: list[int] | None = []


# 删除用户
class UserDeleteIn(BaseModel):
    """
    用户删除模型
    """

    id: int | None = None
    email: str | None = None
