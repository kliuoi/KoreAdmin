from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, func
from typing import Annotated
from datetime import datetime


# 通用 Mapped 类型主键
id_key = Annotated[
    int,
    mapped_column(init=False, primary_key=True, index=True, autoincrement=True, sort_order=-999),
]


class DateTimeMixin(MappedAsDataclass):
    """
    声明日期时间数据类映射

    MappedAsDataclass:
    https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses
    """

    __abstract__ = True

    create_datetime: Mapped[datetime | None] = mapped_column(
        DateTime, init=False, server_default=func.now(), comment="创建时间"
    )
    update_datetime: Mapped[datetime | None] = mapped_column(
        DateTime, init=False, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )
    # TODO 软删除的相关查询时逻辑需要补充
    delete_datetime: Mapped[datetime | None] = mapped_column(DateTime, init=False, nullable=True, comment="删除时间")
    is_delete: Mapped[bool] = mapped_column(Boolean, init=False, default=False, comment="是否软删除")


class MappedBase(DeclarativeBase):
    """
    声明基本的模型类

    Sqlalchemy新版本中, 使用类方法声明替代了函数声明, 参考:
    https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#step-one-orm-declarative-base-is-superseded-by-orm-declarativebase

    DeclarativeBase详细参考:
    https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html

    mapped_column(), API参考:
    https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column

    """

    __abstract__ = True


class Base(DateTimeMixin, MappedBase):
    """
    与数据类映射集成
    """

    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    # id: Mapped[id_key] = mapped_column(init=False, comment="主键id")


class Sys_Casbin_Rule(MappedBase):
    """重写 casbin 中的 CasbinRule model 类, 使用自定义Base, 避免产生 alembic 迁移问题"""

    __tablename__: str = "sys_casbin_rule"
    __table_args__ = {"extend_existing": True, "comment": "Casbin规则表"}

    id: Mapped[int] = mapped_column(primary_key=True)
    ptype: Mapped[str] = mapped_column(comment="规则类型: p/g")
    v0: Mapped[str] = mapped_column(comment="规则名称")
    v1: Mapped[str] = mapped_column(comment="请求资源/规则名称")
    v2: Mapped[str | None] = mapped_column(comment="请求方法")
    v3: Mapped[str | None] = mapped_column()
    v4: Mapped[str | None] = mapped_column()
    v5: Mapped[str | None] = mapped_column()
