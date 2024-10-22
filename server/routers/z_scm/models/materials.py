from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.db.models import Base, id_key


# 物料模型
class Materials(Base):
    __tablename__: str = "materials"
    __table_args__ = {"comment": "物料表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)
    # 新物料编码
    material_code: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    # 名称
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    # 规格
    specification: Mapped[str] = mapped_column(nullable=False)
    # 材料
    material: Mapped[str] = mapped_column(nullable=True)
    # 厚度
    thickness: Mapped[str] = mapped_column(nullable=True)
    # 工艺
    process: Mapped[str] = mapped_column(nullable=True)
    # 项目
    project: Mapped[str] = mapped_column(nullable=False)
    # 商品单位
    unit: Mapped[str] = mapped_column(nullable=False)
    # 发图日期
    send_date: Mapped[str] = mapped_column(nullable=True)
    # 交样日期
    sample_date: Mapped[str] = mapped_column(nullable=True)
    # 供应商价格未税
    supplier_price_without_tax: Mapped[str] = mapped_column(nullable=True)
    # 客户价格已税
    customer_price_with_tax: Mapped[str] = mapped_column(nullable=True)
    # 是否验证通过
    is_verified: Mapped[str] = mapped_column(default=False)
    # 是否签承认书
    has_recognition: Mapped[str] = mapped_column(default=False)
    # 是否量产做货
    is_mass_production: Mapped[str] = mapped_column(default=False)
    # 对接客户
    contact_customer: Mapped[str] = mapped_column(nullable=True)
    # 备注
    remark: Mapped[str] = mapped_column(nullable=True)
