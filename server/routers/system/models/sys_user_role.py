from sqlalchemy import Table, ForeignKey, Column, Integer

from server.db.models import Base


Sys_User_Role = Table(
    "sys_user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("sys_user.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("sys_role.id", ondelete="CASCADE"), primary_key=True),
    comment="用户角色表",
)
