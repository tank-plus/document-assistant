from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for

from form.form import *
from model.order import Order
from route.common import login_required
from model.customer import Customer
from model.product import Product

order_bp = Blueprint('order', __name__)


@order_bp.route('/')
@login_required
def order_list():
    items = Order.query.all()
    return render_template('order.html', items=items)


@order_bp.route('/preview/<order_id>')
@login_required
def order_preview(order_id):
    order = Order.query.get(order_id)
    order_details = OrderDetail.query.filter(OrderDetail.order_id == order_id, OrderDetail.type == '商品').all()
    part_details = OrderDetail.query.filter(OrderDetail.order_id == order_id, OrderDetail.type == '配件').all()
    pallets = Pallet.query.filter(Pallet.order_id == order_id).all()
    order.order_details = order_details
    order.part_details = part_details
    order.pallets = pallets
    return render_template('order_preview.html', order=order)


@order_bp.route('/add')
@login_required
def order_add():
    current_year = datetime.now().year
    start_data = datetime(current_year, 1, 1)
    end_data = datetime(current_year, 12, 31)
    order_count = Order.query.filter(Order.po_date.between(start_data, end_data)).count()
    pi_num = f'NBHB/RFC{current_year % 100}{order_count + 1:02}'  # 看是跟着客户走，还是就订单数走
    customers = Customer.query.all()
    products = Product.query.filter(Product.is_parts == False).all()
    parts = Product.query.filter(Product.is_parts == True).all()
    form = OrderForm()
    form.port_of_loading.data = 'NINGBO, CHINA'
    form.port_of_destination.data = 'MONTREAL, CANADA'
    form.pi_num.data = pi_num  # 当年的第N个订单
    form.order_details.append_entry(OrderDetailForm())  # 默认带一个商品
    form.order_details.append_entry(OrderDetailForm())  # 默认带一个商品
    form.order_details.append_entry(OrderDetailForm())  # 默认带一个商品
    form.part_details.append_entry(OrderDetailForm())  # 默认带一个零件
    form.pallets.append_entry(PalletForm())  # 默认带一个托盘
    return render_template('order_submit.html', form=form, customers=customers, products=products, parts=parts)


@order_bp.route('/order_submit', methods=['GET', 'POST'])
@login_required
def order_save():
    form = OrderForm()
    order_data: Order = form.build_order()
    Order.insert_order(order_data)
    return redirect(url_for('order.order_list'))


@order_bp.route('/delete/<id>', methods=['POST'])
@login_required
def order_delete(id):
    return redirect(url_for('order.order_list'))
