from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from model.db import db

app = Flask(__name__)
# 配置数据库URI，请根据实际情况替换以下字符串
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///order_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'template_secret_key'  # 用于安全地签名session
db.init_app(app)

# Model定义
from model.user import *
from model.customer import *
from model.product import *
from model.order import *
from model.inspect import *
from model.clearance import *
from model.address import *

# 以上是Model定义


# 创建数据库（第一次运行时取消注释）
with app.app_context():
    db.create_all()

# api接口定义
from flask_restx import Api
from api.order import order_ns
from api.chatbot import chatbot_ns

api = Api(app, version='1.0', title='单证自助系统', description='单证自助系统API')
api.add_namespace(order_ns)
api.add_namespace(chatbot_ns)
# 以上是api接口定义


# 通用路由定义
from route.common import login_required


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 假设有一个验证用户的函数validate(username, password)
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "admin":  # 假设这是你的验证函数
            session['logged_in'] = True
            session['current_user'] = username
            return redirect(url_for('index'))
        else:
            pass
    return render_template('login.html')


@app.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')


@app.route('/index')
@login_required
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/add', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    if username and email:
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update_user():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    if user:
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('current_user', None)
    session.clear()
    return redirect(url_for('login'))

@app.template_filter('format_currency')
def format_currency(value):
    return f"{value:.2f}"

# 以上是通用路由定义

# 业务路由定义  
from route.customer import customer_bp

app.register_blueprint(customer_bp, url_prefix='/customer')

from route.product import product_bp

app.register_blueprint(product_bp, url_prefix='/product')

from route.order import order_bp

app.register_blueprint(order_bp, url_prefix='/order')

from route.inspect import inspect_bp

app.register_blueprint(inspect_bp, url_prefix='/inspect')

from route.clearance import clearance_bp

app.register_blueprint(clearance_bp, url_prefix='/clearance')

from route.user import user_bp

app.register_blueprint(user_bp, url_prefix='/user')
# 以上是业务路由定义

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)
