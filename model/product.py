from model.db import db


class Product(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # 产品编号
    model_category = db.Column(db.String(80), unique=False, nullable=False)  # 型号
    unit_price = db.Column(db.Float, unique=False, nullable=False)  # 单价，每年会根据汇率调整
    nw_kgs = db.Column(db.Float, unique=False, nullable=False)  # 净重
    gw_kgs = db.Column(db.Float, unique=False, nullable=False)  # 毛重
    length = db.Column(db.Float, unique=False, nullable=False)  # 长
    width = db.Column(db.Float, unique=False, nullable=False)  # 宽
    height = db.Column(db.Float, unique=False, nullable=False)  # 高
    mt_cmb = db.Column(db.Float, unique=False, nullable=False)  # 体积
    pcs_cnts_ratio = db.Column(db.Integer, unique=False, nullable=False)  # 产品件箱系数
    pcs_per_cnt = db.Column(db.Integer, unique=False, nullable=False)  # 装箱量，即每个集装箱能装多少件产品
    hs_code = db.Column(db.String(80), unique=False, nullable=False)  # 报关时的商品编号
    is_parts = db.Column(db.Boolean, unique=False, nullable=False)  # 是否配件
    remarks = db.Column(db.String(4096), unique=False, nullable=True)

    def __repr__(self):
        return '<Product %r>' % self.model_id
