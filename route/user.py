
from flask import Blueprint, render_template, request, redirect, url_for
from model.user import User
from model.db import db
from route.common import login_required
user_bp = Blueprint('user', __name__)

@user_bp.route('/')
@login_required
def user():
    items = User.query.all()
    return render_template('user.html', items=items)

@user_bp.route('/add')
@login_required
def user_add():
    return render_template('user_edit.html')
    
    
@user_bp.route('/save', methods=['POST'])
@login_required
def user_save():
    return redirect(url_for('user.user'))
    
    
@user_bp.route('/delete/<id>')
@login_required
def user_delete(id):
    return redirect(url_for('user.user'))
