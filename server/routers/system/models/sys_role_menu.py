from sqlalchemy import Table, ForeignKey, Column, Integer

from server.db.models import Base


Sys_Role_Menu = Table(
    "sys_role_menu",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("sys_role.id", ondelete="CASCADE"), primary_key=True),
    Column("menu_id", Integer, ForeignKey("sys_menu.id", ondelete="CASCADE"), primary_key=True),
    comment="角色菜单表",
)
