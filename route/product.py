from flask import Blueprint, render_template, request, redirect, url_for
from model.product import Product
from model.db import db
from route.common import login_required

product_bp = Blueprint('product', __name__)


@product_bp.route('/')
@login_required
def product_list():
    items = Product.query.all()
    return render_template('product.html', items=items)


@product_bp.route('/add')
@login_required
def product_add():
    id = request.args.get('id')
    action = request.args.get('action')
    if id:
        item = Product.query.get(id)
        return render_template('product_edit.html', item=item, action=action)
    else:
        return render_template('product_edit.html', item={}, action=action)


@product_bp.route('/save', methods=['POST'])
def product_save():
    id = request.form.get('id')  # 产品编号
    model_category = request.form.get('model_category')  # 产品型号
    unit_price = float(request.form.get('unit_price'))  # 单价
    nw_kgs = float(request.form.get('nw_kgs'))  # 净重
    gw_kgs = float(request.form.get('gw_kgs'))  # 毛重
    length = request.form.get("length")  # 长
    width = request.form.get('width')  # 宽
    height = request.form.get('height')  # 高
    remarks = request.form.get('remarks')  # 备注
    mt_cmb = float(request.form.get('mt_cmb'))  # 体积
    pcs_cnts_ratio = int(request.form.get('pcs_cnts_ratio'))  # 件箱系数
    pcs_per_cnt = int(request.form.get('pcs_per_cnt'))  # 装箱量
    hs_code = request.form.get('hs_code')  # 报关时的商品编号
    hs_us_code = request.form.get('hs_us_code')
    if 'true' == request.form.get('is_parts'):
        is_parts = True
    else:
        is_parts = False
    product = Product.query.get(id)
    if not product:
        product = Product(id=id, model_category=model_category, unit_price=unit_price, nw_kgs=nw_kgs, gw_kgs=gw_kgs,
                          length=length, width=width, height=height, mt_cmb=mt_cmb, pcs_cnts_ratio=pcs_cnts_ratio,
                          pcs_per_cnt=pcs_per_cnt, hs_code=hs_code, hs_us_code=hs_us_code, is_parts=is_parts,
                          remarks=remarks)
        db.session.add(product)
        db.session.commit()
    else:
        product.model_category = model_category
        product.unit_price = unit_price
        product.nw_kgs = nw_kgs
        product.gw_kgs = gw_kgs
        product.length = length
        product.width = width
        product.height = height
        product.mt_cmb = mt_cmb
        product.pcs_cnts_ratio = pcs_cnts_ratio
        product.pcs_per_cnt = pcs_per_cnt
        product.hs_code = hs_code
        product.hs_us_code = hs_us_code
        product.is_parts = is_parts
        product.remarks = remarks
        db.session.commit()
    return redirect(url_for('product.product_list'))


@product_bp.route('/delete/<id>', methods=['POST'])
def product_delete(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('product.product_list'))
