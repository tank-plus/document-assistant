from model.db import db


class Customer(db.Model):
    id = db.Column(db.String(80), primary_key=True)  # 客户编号
    alias_name = db.Column(db.String(80), unique=False, nullable=False)  # 客户别名
    short_name = db.Column(db.String(80), unique=False, nullable=False)  # 客户简称
    address = db.Column(db.String(4096), unique=False, nullable=False)  # 客户地址
    country = db.Column(db.String(80), unique=False, nullable=False)  # 国家
    country_short_name = db.Column(db.String(80), unique=False, nullable=False)  # 国家缩写
    tel_fax = db.Column(db.String(80), unique=False, nullable=True)  # Tel/Fax
    remarks = db.Column(db.String(4096), unique=False, nullable=True)  # 备注

    def __repr__(self):
        return '<Customer %r>' % self.id
