from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.db.models import Base, id_key


# 公司实体模型
class Customers(Base):
    __tablename__: str = "customers"
    __table_args__ = {"comment": "公司实体表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)
    # 公司名称
    company_name: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    # 对接人
    contact_person: Mapped[str] = mapped_column(nullable=False)
    # 对接手机号
    phone: Mapped[str] = mapped_column(nullable=True)
    # 对接邮箱
    email: Mapped[str] = mapped_column(nullable=True)
    # 公司地址
    address: Mapped[str] = mapped_column(nullable=True)
    # 备注
    remark: Mapped[str] = mapped_column()

    # 与物料模型关联
    materials: Mapped[list["Materials"]] = relationship(init=False, back_populates="contact_customer")  # type: ignore # noqa: F821
