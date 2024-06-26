from model.db import db

class InspectDeclaration(db.Model):
    id = db.Column(db.String(36), primary_key=True) # 编号
    create_date = db.Column(db.Date, unique=False, nullable=False) # 创建日期
    confirm_inspect_date = db.Column(db.Date, unique=False, nullable=False) # 确认商检日期
    cofirm_declare_date = db.Column(db.Date, unique=False, nullable=False) # 确认报关日期
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False) # 地址ID
    bl_num = db.Column(db.String(80), unique=False, nullable=False) # 提运单号
    remarks = db.Column(db.String(4096), unique=False, nullable=True) # 备注


class InspectDeclarationOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 编号
    declaration_id = db.Column(db.String(36), db.ForeignKey('inspect_declaration.id'), nullable=False) # 商检报关编号
    order_id = db.Column(db.String(36), db.ForeignKey('order.po_num'), nullable=False) # 订单编号
