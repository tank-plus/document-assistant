from model.db import db
from core.constant import *


class OrderDetail(db.Model):
    order_id = db.Column(db.String(36), db.ForeignKey('order.po_num'), primary_key=True)  # 订单编号
    product_id = db.Column(db.String(36), db.ForeignKey('product.id'), primary_key=True)  # 产品编号
    product_model = db.Column(db.String(80), nullable=False)  # 产品型号 取-分隔后前面那部分
    qty = db.Column(db.Integer, nullable=False)  # 数量
    type = db.Column(db.String(80), nullable=False)  # 类型 普通商品/配件
    unit_price = db.Column(db.Float, nullable=False)  # 单价
    total_price = db.Column(db.Float, nullable=False)  # 总价
    ctns = db.Column(db.Integer, nullable=False)  # 集装箱数量
    nw_kgs = db.Column(db.Float, nullable=False)  # 净重
    gw_kgs = db.Column(db.Float, nullable=False)  # 毛重
    mt_cmb = db.Column(db.Float, nullable=False)  # 体积

    def __repr__(self):
        return '<OrderDetail %r>' % self.order_id


class Pallet(db.Model):  # 托盘没有价格，有体积、净重和重
    order_id = db.Column(db.String(36), db.ForeignKey('order.po_num'), primary_key=True)  # 订单编号
    name = db.Column(db.String(80), nullable=False)  # 托盘名称
    width = db.Column(db.Float, nullable=False)  # 宽
    height = db.Column(db.Float, nullable=False)  # 高
    length = db.Column(db.Float, nullable=False)  # 长
    nw_kgs = db.Column(db.Float, nullable=False)  # 净重
    gw_kgs = db.Column(db.Float, nullable=False)  # 毛重
    mt_cmb = db.Column(db.Float, nullable=False)  # 体积
    qty = db.Column(db.Integer, nullable=False)  # 数量
    total_mt_cmb = db.Column(db.Float, nullable=False)  # 总体积
    total_nw_kgs = db.Column(db.Float, nullable=False)  # 总净重
    total_gw_kgs = db.Column(db.Float, nullable=False)  # 总毛重


class Order(db.Model):
    po_num = db.Column(db.String(36), primary_key=True)  # 订单编号
    customer_id = db.Column(db.String(80), db.ForeignKey('customer.id'), nullable=False)  # 客户编号
    pi_num = db.Column(db.String(36), nullable=False)  # PI编号
    po_date = db.Column(db.Date, nullable=False)  # 订单日期
    payment_method = db.Column(db.String(80), nullable=False)  # 付款方式
    delivery_date = db.Column(db.Date, nullable=False)  # 交货日期
    port_of_loading = db.Column(db.String(80), nullable=False)  # 装运港
    port_of_destination = db.Column(db.String(80), nullable=False)  # 目的港
    ctn_size_qty = db.Column(db.Float, nullable=True)  # 集装箱尺寸
    billing_of_loading_num = db.Column(db.String(80), nullable=True)  # 装运单号
    ctn_num = db.Column(db.String(80), nullable=True)  # 集装箱号
    seal_num = db.Column(db.String(80), nullable=True)  # 铅封号
    lot = db.Column(db.Date, nullable=False)  # LOT时间
    workshop = db.Column(db.String(80), nullable=True)  # 车间名
    batch_num = db.Column(db.String(80), nullable=True)  # 批号
    status = db.Column(db.String(80), nullable=False)  # 订单状态
    created_at = db.Column(db.DateTime, default=db.func.now())  # 创建时间
    remarks = db.Column(db.String(4096), nullable=True)  # 备注

    def update_status(self, status):
        self.status = status
        db.session.commit()

    def confirm(self):
        # TODO 根据模板生成excel
        self.status = ORDER_STATUS_CONFIRMED
        db.session.commit()

    @staticmethod
    def insert_order(order):
        order_details = []
        for order_detail in order.order_details:
            order_details.append(order_detail)
        db.session.add_all(order_details)

        part_details = []
        for part_detail in order.part_details:
            part_details.append(part_detail)
        db.session.add_all(part_details)

        pallets = []
        for pallet in order.pallets:
            pallets.append(pallet)
        db.session.add_all(pallets)
        order.status = ORDER_STATUS_INIT
        db.session.add(order)
        db.session.commit()

    @staticmethod
    def get_order_by_po_num(po_num):
        order_details = OrderDetail.query.filter_by(order_id=po_num, type="商品").all()
        part_details = OrderDetail.query.filter_by(order_id=po_num, type="配件").all()
        pallets = Pallet.query.filter_by(order_id=po_num).all()
        order = Order.query.get(po_num)
        order.order_details = order_details
        order.part_details = part_details
        order.pallets = pallets
        return order

    def __repr__(self):
        return '<Order %r>' % self.po_num
