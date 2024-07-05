from flask import Blueprint, flash, render_template, request, redirect, url_for
from model.order import *
from model.db import db
from route.common import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , FloatField, DateField, FieldList, FormField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime


order_bp = Blueprint('order', __name__)
    
class OrderDetailForm(FlaskForm):
    product_id = StringField('产品编号')
    qty = FloatField('数量')
    type = StringField('类型')

class PalletForm(FlaskForm):
    name = StringField('托盘名称')
    width = FloatField('宽')
    height = FloatField('高')
    length = FloatField('长')
    nw_kgs = FloatField('净重')
    gw_kgs = FloatField('毛重')
    mt_cmb = FloatField('体积')
    qty = FloatField('数量')
    total_mt_cmb = FloatField('总体积')
    total_nw_kgs = FloatField('总净重')
    total_gw_kgs = FloatField('总毛重')
    
class OrderForm(FlaskForm):
    po_num = StringField('订单编号')
    customer_id = StringField('客户编号')
    pi_num = StringField('PI编号')
    po_date = DateField('订单日期', format='%Y-%m-%d')
    payment_method = StringField('付款方式')
    delivery_date = DateField('交货日期', format='%Y-%m-%d')
    port_of_loading = StringField('装运港')
    port_of_destination = StringField('目的港')
    ctn_size_qty = FloatField('集装箱尺寸')
    billing_of_loading_num = StringField('装运单号')
    ctn_num = StringField('集装箱号')
    seal_num = StringField('铅封号')
    lot = DateField('LOT日期')
    workshop = StringField('车间名')
    batch_num = StringField('批次号')
    remarks = TextAreaField('备注')
    order_details = FieldList(FormField(OrderDetailForm))
    part_details = FieldList(FormField(OrderDetailForm))
    pallets = FieldList(FormField(PalletForm))

@order_bp.route('/')
@login_required
def order():
    items = Order.query.all()
    return render_template('order.html', items=items)

@order_bp.route('/add')
@login_required
def order_add():
    form = OrderForm()
    form.order_details.append_entry(OrderDetailForm())
    form.port_of_loading.data = 'NINGBO, CHINA'
    form.port_of_destination.data = 'MONTREAL, CANADA'
    form.pi_num.data = 'NBHB/RFC2331' # 当年的第N个订单
    # form.part_details.append_entry(OrderDetailForm())
    form.pallets.append_entry(PalletForm())
    return render_template('order_submit.html', form=form)
    
    
@order_bp.route('/order_submit', methods=['GET','POST'])
@login_required
def order_save():
    form = OrderForm()
    order = Order(
        # 主Order字段...
    )
    # db.session.add(order)

    for detail_form in form.order_details.data:
        order_detail = OrderDetail(
            order_id=order.po_num,  # 假设Order的PO编号是创建后立即可用的
            product_id=detail_form['product_id'],
            qty=detail_form['qty'],
            type=detail_form['type']
        )
        # db.session.add(order_detail)
        
    for part_form in form.part_details.data:
        order_detail = OrderDetail(
            order_id=order.po_num,  # 假设Order的PO编号是创建后立即可用的
            product_id=part_form['product_id'],
            qty=part_form['qty'],
            type=part_form['type']
        )

    for pallet_form in form.pallets.data:
        pallet = Pallet(
            order_id=order.po_num,
            # Pallet的字段...
        )
        # db.session.add(pallet)

    # db.session.commit()
    # flash('订单创建成功')
    return redirect(url_for('order.order'))
   
    
    
    
@order_bp.route('/delete/<id>')
@login_required
def order_delete(id):
    return redirect(url_for('order.order'))