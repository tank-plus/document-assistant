from flask_restx import Namespace, Resource, fields
from core.util import *

order_ns = Namespace('order', description='Order related operations')

@order_ns.route('/<string:order_id>')
class OrderConfirm(Resource):

    @order_ns.doc('confirm_order')
    @wrap_response
    def post(self, order_id):
        return "success"