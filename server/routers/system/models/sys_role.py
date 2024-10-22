from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.db.models import Base, id_key

from .sys_user_role import Sys_User_Role
from .sys_role_menu import Sys_Role_Menu


class Sys_Role(Base):
    __tablename__: str = "sys_role"
    __table_args__ = {"comment": "角色表"}

    id: Mapped[id_key] = mapped_column(init=False, comment="主键id")
    name: Mapped[str] = mapped_column(nullable=False, unique=True, comment="角色名称")
    enable: Mapped[bool] = mapped_column(nullable=False, index=True, default=True, comment="是否启用")
    description: Mapped[str | None] = mapped_column(default=None, comment="角色描述")

    # 用户多对多
    users: Mapped[set["Sys_User"]] = relationship(init=False, secondary=Sys_User_Role, back_populates="roles")  # type: ignore # noqa: F821

    # 菜单多对多
    menus: Mapped[set["Sys_Menu"]] = relationship(init=False, secondary=Sys_Role_Menu, back_populates="roles")  # type: ignore # noqa: F821

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Sys_Role):
            return self.id == other.id
        return False
