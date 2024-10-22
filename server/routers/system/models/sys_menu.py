from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Union

from server.db.models import Base, id_key

from .sys_role_menu import Sys_Role_Menu


class Sys_Menu(Base):
    """菜单模型"""

    __tablename__: str = "sys_menu"
    __table_args__ = {"comment": "菜单表"}

    id: Mapped[id_key] = mapped_column(init=False, comment="主键id")
    name: Mapped[str] = mapped_column(comment="菜单标题")
    type: Mapped[str] = mapped_column(comment="菜单类型")
    path: Mapped[str | None] = mapped_column(default=None, comment="请求路径")
    method: Mapped[str | None] = mapped_column(default=None, comment="请求方法")
    perms: Mapped[str | None] = mapped_column(default=None, comment="权限标识")
    icon: Mapped[str | None] = mapped_column(default=None, comment="菜单图标")
    order: Mapped[int | None] = mapped_column(default=None, comment="排序")
    disabled: Mapped[bool] = mapped_column(default=False, comment="是否禁用")

    # 父级菜单
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("sys_menu.id", ondelete="SET NULL"), default=None, comment="父级ID"
    )
    parent: Mapped[Union["Sys_Menu", None]] = relationship(init=False, back_populates="children", remote_side=[id])
    children: Mapped[list["Sys_Menu"] | None] = relationship(init=False, back_populates="parent")

    # 角色多对多
    roles: Mapped[set["Sys_Role"]] = relationship(init=False, secondary=Sys_Role_Menu, back_populates="menus")  # type: ignore # noqa: F821
