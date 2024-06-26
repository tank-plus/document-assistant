from flask import Blueprint, render_template, request, redirect, url_for
from model.product import Product
from model.db import db
from route.common import login_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
@login_required
def product():
    items = Product.query.all()
    return render_template('product.html', items=items)

@product_bp.route('/add')
@login_required
def product_add():
    return render_template('product_edit.html')


@product_bp.route('/save', methods=['POST'])
def product_save():
    id = request.form.get('id') # 产品编号
    model_category = request.form.get('model_category') #产品型号
    unit_price = float(request.form.get('unit_price')) # 单价
    nw_kgs = float(request.form.get('nw_kgs')) # 净重
    gw_kgs = float(request.form.get('gw_kgs')) # 毛重
    length = request.form.get("length") # 长
    width = request.form.get('width') # 宽
    height = request.form.get('height') # 高
    remarks = request.form.get('remarks') # 备注
    mt_cmb = float(request.form.get('mt_cmb')) # 体积
    pcs_cnts_ratio = int(request.form.get('pcs_cnts_ratio')) #件箱系数
    pcs_per_cnt = int(request.form.get('pcs_per_cnt')) # 装箱量
    hs_code = request.form.get('hs_code') # 报关时的商品编号
    is_parts = bool(request.form.get('is_parts')) # 是否配件
    if not is_parts:
        is_parts = False
    product = Product(id=id, model_category=model_category, unit_price=unit_price, nw_kgs=nw_kgs, gw_kgs=gw_kgs,length=length, width=width, height=height, mt_cmb=mt_cmb, pcs_cnts_ratio=pcs_cnts_ratio, pcs_per_cnt=pcs_per_cnt, hs_code=hs_code, is_parts=is_parts, remarks=remarks)
    db.session.add(product)
    db.session.commit()
    return redirect(url_for('product.product'))

@product_bp.route('/delete/<id>', methods=['POST'])
def product_delete(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('product.product'))