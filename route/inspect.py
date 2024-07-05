from flask import Blueprint, render_template, request, redirect, url_for
from model.inspect import *
from model.db import db
from route.common import login_required

inspect_bp = Blueprint('inspect', __name__)


@inspect_bp.route('/')
@login_required
def inspectdeclaration():
    items = InspectDeclaration.query.all()
    return render_template('inspectdeclaration.html', items=items)


@inspect_bp.route('/add')
@login_required
def inspectdeclaration_add():
    return render_template('inspectdeclaration_edit.html')


@inspect_bp.route('/save', methods=['POST'])
@login_required
def inspectdeclaration_save():
    return redirect(url_for('inspect.inspect'))


@inspect_bp.route('/delete/<id>')
@login_required
def inspectdeclaration_delete(id):
    return redirect(url_for('inspect.inspect'))
