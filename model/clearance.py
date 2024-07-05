from model.db import db


class Clearance(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # 编号
    create_date = db.Column(db.Date, unique=False, nullable=False)  # 创建日期
    confirm_clearance_date = db.Column(db.Date, unique=False, nullable=False)  # 确认结关日期
    ctnr_no = db.Column(db.String(80), unique=False, nullable=False)  # 集装箱号
    seal_no = db.Column(db.String(80), unique=False, nullable=False)  # 铅封号
    remarks = db.Column(db.String(4096), unique=False, nullable=True)  # 备注


class ClearanceInspect(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 编号
    clearance_id = db.Column(db.String(36), db.ForeignKey('clearance.id'), nullable=False)  # 结关编号
    inspect_id = db.Column(db.String(36), db.ForeignKey('inspect_declaration.id'), nullable=False)  # 商检报关编号


class ClearanceOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 编号
    clearance_id = db.Column(db.String(36), db.ForeignKey('clearance.id'), nullable=False)  # 结关编号
    order_id = db.Column(db.String(36), db.ForeignKey('order.po_num'), nullable=False)  # 订单编号
