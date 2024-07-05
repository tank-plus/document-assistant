from flask import Blueprint, render_template, request, redirect, url_for
from model.clearance import *
from model.db import db
from route.common import login_required

clearance_bp = Blueprint('clearance', __name__)


@clearance_bp.route('/')
@login_required
def clearance():
    items = Clearance.query.all()
    return render_template('clearance.html', items=items)


@clearance_bp.route('/add')
@login_required
def clearance_add():
    return render_template('clearance_edit.html')


@clearance_bp.route('/save', methods=['POST'])
@login_required
def clearance_save():
    return redirect(url_for('clearance.clearance'))


@clearance_bp.route('/delete/<id>')
@login_required
def clearance_delete(id):
    return redirect(url_for('clearance.clearance'))
