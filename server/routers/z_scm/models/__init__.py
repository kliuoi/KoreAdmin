from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.db.models import Base, id_key


# 公司实体模型
class Customers(Base):
    __tablename__: str = "customers"
    __table_args__ = {"comment": "公司实体表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)
    # 公司名称
    company_name: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    # 公司类型：1-客户，2-供应商
    company_type: Mapped[int] = mapped_column(nullable=False)
    # 对接人
    contact_person: Mapped[str] = mapped_column(nullable=False)
    # 对接联系方式
    contact_phone: Mapped[str] = mapped_column(nullable=False)
    # 备注
    remark: Mapped[str] = mapped_column()


# 物料模型
class Materials(Base):
    __tablename__: str = "materials"
    __table_args__ = {"comment": "物料表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)
    # 归属项目
    project: Mapped[str] = mapped_column(index=True, nullable=False)
    # 新物料编码
    material_code: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    # 名称
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    # 是否允许下单
    is_order: Mapped[str] = mapped_column(default=True)


# 物料明细模型
class MaterialDetails(Base):
    __tablename__: str = "material_details"
    __table_args__ = {"comment": "物料明细表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)

    # TODO关联物料

    # 规格
    specification: Mapped[str] = mapped_column(nullable=False)
    # 材料
    material: Mapped[str] = mapped_column(nullable=True)
    # 厚度
    thickness: Mapped[str] = mapped_column(nullable=True)
    # 工艺
    process: Mapped[str] = mapped_column(nullable=True)
    # 商品单位
    unit: Mapped[str] = mapped_column(nullable=False)
    # 发图日期
    send_date: Mapped[str] = mapped_column(nullable=True)
    # 交样日期
    sample_date: Mapped[str] = mapped_column(nullable=True)
    # 是否验证通过
    is_verified: Mapped[str] = mapped_column(default=False)
    # 是否签承认书
    has_recognition: Mapped[str] = mapped_column(default=False)
    # 是否量产做货
    is_mass_production: Mapped[str] = mapped_column(default=False)
    # 备注
    remark: Mapped[str] = mapped_column(nullable=True)

    # TODO对接供应商
    contact_customer: Mapped[str] = mapped_column(nullable=True)


# 图纸模型
class Drawings(Base):
    __tablename__: str = "drawings"
    __table_args__ = {"comment": "图纸表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)
    # 图纸编号
    drawing_code: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    # 图纸名称
    drawing_name: Mapped[str] = mapped_column(index=True, nullable=False)
    # 图纸类型
    drawing_type: Mapped[str] = mapped_column(nullable=False)
    # 图纸路径
    drawing_path: Mapped[str] = mapped_column(nullable=False)
    # 图纸描述
    drawing_description: Mapped[str] = mapped_column(nullable=True)
    # 备注
    remark: Mapped[str] = mapped_column(nullable=True)


# 订单模型
class Orders(Base):
    __tablename__: str = "orders"
    __table_args__ = {"comment": "订单表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)
    # 订单编号
    order_code: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    # 订单名称
    order_name: Mapped[str] = mapped_column(index=True, nullable=False)
    # 订单类型：1-销售订单，2-采购订单
    order_type: Mapped[str] = mapped_column(nullable=False)
    # 订单状态
    order_status: Mapped[str] = mapped_column(nullable=False)

    # TODO关联公司

    # 订单金额
    order_amount: Mapped[str] = mapped_column(nullable=False)
    # 订单日期
    order_date: Mapped[str] = mapped_column(nullable=False)
    # 备注
    remark: Mapped[str] = mapped_column(nullable=True)


# 订单明细模型
class OrderDetails(Base):
    __tablename__: str = "order_details"
    __table_args__ = {"comment": "订单明细表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)

    # TODO关联订单
    # TODO关联物料

    # 数量
    quantity: Mapped[str] = mapped_column(nullable=False)
    # 单价
    unit_price: Mapped[str] = mapped_column(nullable=False)
    # 金额
    amount: Mapped[str] = mapped_column(nullable=False)
    # 交货日期
    delivery_date: Mapped[str] = mapped_column(nullable=False)
    # 备注
    remark: Mapped[str] = mapped_column(nullable=True)


# 物料库存模型
class MaterialStock(Base):
    __tablename__: str = "material_stock"
    __table_args__ = {"comment": "物料库存表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)

    # TODO关联物料

    # 数量
    quantity: Mapped[str] = mapped_column(nullable=False)
    # 备注
    remark: Mapped[str] = mapped_column(nullable=True)


# 物料送货模型
class MaterialDelivery(Base):
    __tablename__: str = "material_delivery"
    __table_args__ = {"comment": "物料送货表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)
    # 送货单号
    delivery_code: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    # 送货日期
    delivery_date: Mapped[str] = mapped_column(nullable=False)

    # TODO关联供物料

    # 数量
    quantity: Mapped[str] = mapped_column(nullable=False)
    # 单价
    unit_price: Mapped[str] = mapped_column(nullable=False)
    # 金额
    amount: Mapped[str] = mapped_column(nullable=False)
    # 备注
    remark: Mapped[str] = mapped_column(nullable=True)
    # 物料
    material: Mapped[str] = mapped_column(nullable=False)


# 对账单模型
class Reconciliation(Base):
    __tablename__: str = "reconciliation"
    __table_args__ = {"comment": "对账单表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)
    # 对账单号
    reconciliation_code: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    # 对账日期
    reconciliation_date: Mapped[str] = mapped_column(nullable=False)
    # 客户名称
    customer_name: Mapped[str] = mapped_column(nullable=False)
    # 对账金额
    reconciliation_amount: Mapped[str] = mapped_column(nullable=False)
    # 备注
    remark: Mapped[str] = mapped_column(nullable=True)


# 对账单明细模型
class ReconciliationDetails(Base):
    __tablename__: str = "reconciliation_details"
    __table_args__ = {"comment": "对账单明细表"}

    id: Mapped[id_key] = mapped_column(primary_key=True)
    # 对账单号
    reconciliation_code: Mapped[str] = mapped_column(index=True, nullable=False)
    # 订单编号
    order_code: Mapped[str] = mapped_column(index=True, nullable=False)
    # 订单名称
    order_name: Mapped[str] = mapped_column(index=True, nullable=False)
    # 订单金额
    order_amount: Mapped[str] = mapped_column(nullable=False)
    # 对账金额
    reconciliation_amount: Mapped[str] = mapped_column(nullable=False)
    # 备注
    remark: Mapped[str] = mapped_column(nullable=True)
    # 对账单
    reconciliation: Mapped[str] = mapped_column(nullable=False)
    # 订单
    order: Mapped[str] = mapped_column(nullable=False)
