from model.db import db

class Order(db.Model):
    po_num = db.Column(db.String(36), primary_key=True) # 订单编号
    customer_id = db.Column(db.String(80), db.ForeignKey('customer.id'), nullable=False) # 客户编号
    pi_num = db.Column(db.String(36), unique=False, nullable=False) # PI编号
    po_date = db.Column(db.Date, unique=False, nullable=False) # 订单日期
    payment_method = db.Column(db.String(80), unique=False, nullable=False) # 付款方式
    delivery_date = db.Column(db.Date, unique=False, nullable=False) # 交货日期
    port_of_loading = db.Column(db.String(80), unique=False, nullable=False) # 装运港
    port_of_destination = db.Column(db.String(80), unique=False, nullable=False) # 目的港
    ctn_size_qty = db.Column(db.Float, unique=False, nullable=False) # 集装箱尺寸
    billing_of_loading_num = db.Column(db.String(80), unique=False, nullable=False) # 装运单号
    ctn_num = db.Column(db.String(80), unique=False, nullable=False) # 集装箱号
    seal_num = db.Column(db.String(80), unique=False, nullable=False) # 铅封号
    lot = db.Column(db.String(80), unique=False, nullable=False) # 批号
    workshop = db.Column(db.String(80), unique=False, nullable=False) # 车间名
    batch_num = db.Column(db.String(80), unique=False, nullable=False) # 批号
    remarks = db.Column(db.String(4096), unique=False, nullable=True)
    
    def __repr__(self):
        return '<Order %r>' % self.po_num
    
    
class OrderDetail(db.Model):
    order_id = db.Column(db.String(36), db.ForeignKey('order.po_num'), primary_key=True) # 订单编号
    product_id = db.Column(db.String(36), db.ForeignKey('product.id'), primary_key=True) # 产品编号
    qty = db.Column(db.Integer, unique=False, nullable=False) # 数量
    type = db.Column(db.String(80), unique=False, nullable=False) # 类型 普通商品/配件
    
    def __repr__(self):
        return '<OrderDetail %r>' % self.order_id
    
class Pallet(db.Model): # 托盘没有价格，有体积、净重和重
    order_id = db.Column(db.String(36), db.ForeignKey('order.po_num'), primary_key=True) # 订单编号
    name = db.Column(db.String(80), unique=False, nullable=False) # 托盘名称
    width = db.Column(db.Float, unique=False, nullable=False) # 宽
    height = db.Column(db.Float, unique=False, nullable=False) # 高
    length = db.Column(db.Float, unique=False, nullable=False) # 长
    nw_kgs = db.Column(db.Float, unique=False, nullable=False) # 净重
    gw_kgs = db.Column(db.Float, unique=False, nullable=False) # 毛重
    mt_cmb = db.Column(db.Float, unique=False, nullable=False) # 体积
    qty = db.Column(db.Integer, unique=False, nullable=False) # 数量
    total_mt_cmb = db.Column(db.Float, unique=False, nullable=False) # 总体积
    total_nw_kgs = db.Column(db.Float, unique=False, nullable=False) # 总净重
    total_gw_kgs = db.Column(db.Float, unique=False, nullable=False) # 总毛重