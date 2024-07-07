from flask import Blueprint, render_template, request, redirect, url_for
from model.customer import Customer
from model.db import db
from route.common import login_required

customer_bp = Blueprint('customer', __name__)


@customer_bp.route('/')
@login_required
def customer():
    customers = Customer.query.all()
    return render_template('customer.html', customers=customers)


@customer_bp.route('/add')
@login_required
def customer_add():
    id = request.args.get('id')
    action = request.args.get('action')
    if id:
        item = Customer.query.get(id)
        return render_template('customer_edit.html', item=item, action=action)
    else:
        return render_template('customer_edit.html', item={}, action=action)


@customer_bp.route('/save', methods=['POST'])
def customer_save():
    id = request.form.get('id')
    customer_id = request.form.get('customer_id')
    alias_name = request.form.get('alias_name')
    short_name = request.form.get('short_name')
    country = request.form.get('country')
    country_short_name = request.form.get("country_short_name")
    address = request.form.get('address')
    tel_fax = request.form.get('tel_fax')
    remarks = request.form.get('remarks')

    customer_item = Customer.query.get(id)
    if not customer_item:
        customer_item = Customer(customer_id=customer_id, alias_name=alias_name, short_name=short_name, country=country,
                                 country_short_name=country_short_name, address=address, tel_fax=tel_fax,
                                 remarks=remarks)
        db.session.add(customer_item)
        db.session.commit()
    else:
        customer_item.alias_name = alias_name
        customer_item.short_name = short_name
        customer_item.address = address
        customer_item.tel_fax = tel_fax
        customer_item.remarks = remarks
        db.session.commit()
    return redirect(url_for('customer.customer'))


@customer_bp.route('/delete/<customer_id>', methods=['POST'])
def customer_delete(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
    return redirect(url_for('customer.customer'))
