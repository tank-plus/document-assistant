from flask import Blueprint, render_template, request, redirect, url_for
from model.order import Order
from model.db import db
from route.common import login_required

order_bp = Blueprint('order', __name__)

@order_bp.route('/')
@login_required
def order():
    items = Order.query.all()
    return render_template('order.html', items=items)

@order_bp.route('/add')
@login_required
def order_add():
    return render_template('order_edit.html')
    
    
@order_bp.route('/save', methods=['POST'])
@login_required
def order_save():
    return redirect(url_for('order.order'))
    
    
@order_bp.route('/delete/<id>')
@login_required
def order_delete(id):
    return redirect(url_for('order.order'))