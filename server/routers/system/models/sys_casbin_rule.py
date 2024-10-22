# from sqlalchemy.orm import Mapped, mapped_column

# from server.db.models import MappedBase


# class Sys_Casbin_Rule(MappedBase):
#     """重写 casbin 中的 CasbinRule model 类, 使用自定义Base, 避免产生 alembic 迁移问题"""

#     __tablename__: str = "sys_casbin_rule"
#     __table_args__ = {"extend_existing": True}

#     id: Mapped[str] = mapped_column(primary_key=True)
#     ptype: Mapped[str] = mapped_column(comment="规则类型: p/g")
#     v0: Mapped[str] = mapped_column(comment="规则名称")
#     v1: Mapped[str] = mapped_column(comment="请求资源/规则名称")
#     v2: Mapped[str] = mapped_column(comment="请求方法")
#     v3: Mapped[str | None] = mapped_column(default=None)
#     v4: Mapped[str | None] = mapped_column(default=None)
#     v5: Mapped[str | None] = mapped_column(default=None)
