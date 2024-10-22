from sqlalchemy import Table, ForeignKey, Column, Integer

from server.db.models import Base

Sys_User_Dept = Table(
    "sys_user_dept",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("sys_user.id", ondelete="CASCADE"), primary_key=True),
    Column("dept_id", Integer, ForeignKey("sys_dept.id", ondelete="CASCADE"), primary_key=True),
    comment="用户部门表",
)
