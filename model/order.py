from model.db import db
from core.constant import *


class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 订单详情编号
    order_id = db.Column(db.String(36), db.ForeignKey('order.po_num'))  # 订单编号
    product_id = db.Column(db.String(36), db.ForeignKey('product.id'))  # 产品编号
    product_model = db.Column(db.String(80), nullable=True)  # 产品型号 取-分隔后前面那部分
    qty = db.Column(db.Integer, nullable=True)  # 数量
    type = db.Column(db.String(80), nullable=True)  # 类型 普通商品/配件
    unit_price = db.Column(db.Float, nullable=True)  # 单价
    total_price = db.Column(db.Float, nullable=True)  # 总价
    ctns = db.Column(db.Integer, nullable=True)  # 集装箱数量
    nw_kgs = db.Column(db.Float, nullable=True)  # 净重
    gw_kgs = db.Column(db.Float, nullable=True)  # 毛重
    mt_cmb = db.Column(db.Float, nullable=True)  # 体积
    pi_category = db.Column(db.String(80), nullable=True)  # PI类别 FIREPLACE MANTEL/FIREPLACE MANTEL TOPS

    def __repr__(self):
        return '<OrderDetail %r>' % self.order_id


class Pallet(db.Model):  # 托盘没有价格，有体积、净重和重
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 托盘编号
    order_id = db.Column(db.String(36), db.ForeignKey('order.po_num'))  # 订单编号
    name = db.Column(db.String(80), nullable=True)  # 托盘名称
    width = db.Column(db.Float, nullable=True)  # 宽
    height = db.Column(db.Float, nullable=True)  # 高
    length = db.Column(db.Float, nullable=True)  # 长
    nw_kgs = db.Column(db.Float, nullable=True)  # 净重
    gw_kgs = db.Column(db.Float, nullable=True)  # 毛重
    mt_cmb = db.Column(db.Float, nullable=True)  # 体积
    qty = db.Column(db.Integer, nullable=True)  # 数量
    total_mt_cmb = db.Column(db.Float, nullable=True)  # 总体积
    total_nw_kgs = db.Column(db.Float, nullable=True)  # 总净重
    total_gw_kgs = db.Column(db.Float, nullable=True)  # 总毛重


class Order(db.Model):
    po_num = db.Column(db.String(36), primary_key=True)  # 订单编号
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)  # 客户编号
    pi_num = db.Column(db.String(36), nullable=True)  # PI编号
    po_date = db.Column(db.Date, nullable=True)  # 订单日期
    payment_method = db.Column(db.String(80), nullable=True)  # 付款方式
    delivery_date = db.Column(db.String(500), nullable=True)  # 交货日期
    port_of_loading = db.Column(db.String(80), nullable=True)  # 装运港
    port_of_destination = db.Column(db.String(80), nullable=True)  # 目的港
    ctn_size_qty = db.Column(db.Float, nullable=True)  # 集装箱尺寸
    billing_of_loading_num = db.Column(db.String(80), nullable=True)  # 装运单号
    ctn_num = db.Column(db.String(80), nullable=True)  # 集装箱号
    seal_num = db.Column(db.String(80), nullable=True)  # 铅封号
    lot = db.Column(db.Date, nullable=True)  # LOT时间
    workshop = db.Column(db.String(80), nullable=True)  # 车间名
    batch_num = db.Column(db.String(80), nullable=True)  # 批号
    status = db.Column(db.String(80), nullable=True)  # 订单状态
    created_at = db.Column(db.DateTime, default=db.func.now())  # 创建时间
    remarks = db.Column(db.String(4096), nullable=True)  # 备注
    customer = db.relationship('Customer', backref='orders', lazy=True)  # 客户
    order_details = db.relationship('OrderDetail', backref='order', lazy=True)  # 订单详情
    pallets = db.relationship('Pallet', backref='order', lazy=True)  # 托盘

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.order_details = []
        self.part_details = []
        self.pallets = []

    def get_file_name(self):
        date_str = self.po_date.strftime("%Y%m%d")
        product_model_list = [order_detail.product_model for order_detail in self.order_details]
        product_model_str = "_".join(product_model_list)
        return f"PO#{self.po_num}_{product_model_str}_Confirmation_{date_str}.xlsx"

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

    def to_display_data(self):
        display_data = {}
        if self.order_details and len(self.order_details) > 0:
            for order_detail in self.order_details:
                category_name = order_detail.pi_category
                if category_name not in display_data:
                    display_data[category_name] = []
                record = [order_detail.product_id, f"{order_detail.qty}PCS/{order_detail.ctns}CTNS",
                          f"{order_detail.unit_price:.2f}", f"{order_detail.total_price:.2f}"]
                display_data[category_name].append(record)

        if self.part_details and len(self.part_details) > 0:
            for part_detail in self.part_details:
                category_name = part_detail.pi_category
                if category_name not in display_data:
                    display_data[category_name] = []
                record = [part_detail.product_id, f"{part_detail.qty}PCS/{part_detail.ctns}CTNS",
                          f"{part_detail.unit_price:.2f}", f"{part_detail.total_price:.2f}"]
                display_data[category_name].append(record)

        # TODO 托盘如何处理?
        if self.pallets and len(self.pallets) > 0:
            pass

    def __repr__(self):
        return '<Order %r>' % self.po_num
