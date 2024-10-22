from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from datetime import datetime

from server.db.models import Base, id_key
from server.core.utils.timezone import timezone

from .sys_user_dept import Sys_User_Dept
from .sys_user_role import Sys_User_Role


def uuid4_str() -> str:
    """数据库引擎 UUID 类型兼容性解决方案"""
    return str(uuid4())


# 用户模型
class Sys_User(Base):
    """用户模型"""

    __tablename__: str = "sys_user"
    __table_args__ = {"comment": "用户表"}

    id: Mapped[id_key] = mapped_column(init=False, comment="主键id")
    uuid: Mapped[str] = mapped_column(
        init=False, nullable=False, index=True, unique=True, default_factory=uuid4_str, comment="用户UUID"
    )
    email: Mapped[str] = mapped_column(nullable=False, index=True, unique=True, comment="用户登录名")
    password: Mapped[str] = mapped_column(nullable=False, comment="用户登录密码")
    name: Mapped[str | None] = mapped_column(default=None, comment="用户昵称")
    is_active: Mapped[bool] = mapped_column(default=True, comment="是否启用")
    is_admin: Mapped[bool] = mapped_column(default=False, comment="是否为管理员")
    last_login_time: Mapped[datetime | None] = mapped_column(default=None, comment="最后登录时间")
    remark: Mapped[str | None] = mapped_column(default=None, onupdate=timezone.now, comment="用户备注")

    # 用户部门多对多
    depts: Mapped[set["Sys_Dept"]] = relationship(init=False, secondary=Sys_User_Dept, back_populates="users")  # type: ignore # noqa: F821

    # 用户角色多对多
    roles: Mapped[set["Sys_Role"]] = relationship(init=False, secondary=Sys_User_Role, back_populates="users")  # type: ignore # noqa: F821
