from flask_restx import Namespace, Resource, fields
from core.util import *
from model.order import Order, OrderDetail, Pallet
from model.customer import Customer
from core.processor import OrderPIProcessor
from model.db import db

order_ns = Namespace('order', description='Order related operations')

@order_ns.route('/<string:order_id>/confirm')
class OrderConfirm(Resource):

    @order_ns.doc('confirm_order')
    @wrap_response
    def post(self, order_id):
        order = Order.query.get(order_id)
        order_details = OrderDetail.query.filter(OrderDetail.order_id == order_id, OrderDetail.type == '商品').all()
        part_details = OrderDetail.query.filter(OrderDetail.order_id == order_id, OrderDetail.type == '配件').all()
        pallets = Pallet.query.filter(Pallet.order_id == order_id).all()
        order.order_details = order_details
        order.part_details = part_details
        order.pallets = pallets
        customer = Customer.query.get(order.customer_id)
        order.customer = customer
        order_process = OrderPIProcessor(order)
        order_process.process()
        order.status = '已确认'
        order.confirm_file = order_process.target_file_name
        order.order_details.extend(part_details)
        db.session.commit()
        
        return {"file_path": order_process.target_file_name}