from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for

from form.form import *
from model.order import Order
from route.common import login_required

order_bp = Blueprint('order', __name__)


@order_bp.route('/')
@login_required
def order_list():
    items = Order.query.all()
    return render_template('order.html', items=items)


@order_bp.route('/add')
@login_required
def order_add():
    current_year = datetime.now().year
    start_data = datetime(current_year, 1, 1)
    end_data = datetime(current_year, 12, 31)
    order_count = Order.query.filter(Order.order_date.between(start_data, end_data)).count()
    pi_num = f'NBHB/RFC{current_year}{order_count + 1:03}'  # 看是跟着客户走，还是就订单数走
    form = OrderForm()
    form.port_of_loading.data = 'NINGBO, CHINA'
    form.port_of_destination.data = 'MONTREAL, CANADA'
    form.pi_num.data = pi_num  # 当年的第N个订单
    form.order_details.append_entry(OrderDetailForm())  # 默认带一个商品
    form.pallets.append_entry(PalletForm()) # 默认带一个托盘
    return render_template('order_submit.html', form=form)


@order_bp.route('/order_submit', methods=['GET', 'POST'])
@login_required
def order_save():
    form = OrderForm()
    order_data: Order = form.build_order()
    Order.insert_order(order_data)
    return redirect(url_for('order.order'))


@order_bp.route('/delete/<id>')
@login_required
def order_delete(id):
    return redirect(url_for('order.order'))
