from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Union

from server.db.models import Base, id_key

from .sys_user_dept import Sys_User_Dept


class Sys_Dept(Base):
    """部门模型"""

    __tablename__: str = "sys_dept"
    __table_args__ = {"comment": "部门表"}

    id: Mapped[id_key] = mapped_column(init=False, comment="主键id")
    name: Mapped[str] = mapped_column(comment="部门名称")
    sort: Mapped[int | None] = mapped_column(default=None, comment="排序")
    level: Mapped[int | None] = mapped_column(default=None, comment="部门层级")
    disabled: Mapped[bool] = mapped_column(default=False, comment="是否禁用")

    # 父级部门
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("sys_dept.id", ondelete="SET NULL"), default=None, comment="父部门ID"
    )
    parent: Mapped[Union["Sys_Dept", None]] = relationship(init=False, back_populates="children", remote_side=[id])
    children: Mapped[list["Sys_Dept"] | None] = relationship(init=False, back_populates="parent")

    # 修改用户关系为多对多
    users: Mapped[set["Sys_User"]] = relationship(init=False, secondary=Sys_User_Dept, back_populates="depts")  # type: ignore # noqa: F821

    # 关联user的反向关系中是set，为了确保dept是可hash的，添加hash和eq方法，用于在set中进行比较
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Sys_Dept):
            return self.id == other.id
        return False
