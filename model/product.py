from model.db import db
import json

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
    hs_us_code = db.Column(db.String(80), unique=False, nullable=True)  # 国外报关时的商品编号
    remarks = db.Column(db.String(4096), unique=False, nullable=True)

    def __repr__(self):
        return '<Product %r>' % self.model_id

    def to_dict(self):
        return {
            'id': self.id,
            'model_category': self.model_category,
            'unit_price': self.unit_price,
            'nw_kgs': self.nw_kgs,
            'gw_kgs': self.gw_kgs,
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'mt_cmb': self.mt_cmb,
            'pcs_cnts_ratio': self.pcs_cnts_ratio,
            'pcs_per_cnt': self.pcs_per_cnt,
            'hs_code': self.hs_code,
            'is_parts': self.is_parts,
            'hs_us_code': self.hs_us_code,
            'remarks': self.remarks
        }
        
        
    def to_json(self):
        data = self.to_dict()
        return json.dumps(data)