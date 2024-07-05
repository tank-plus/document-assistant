from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, FieldList, FormField, TextAreaField
from wtforms.fields.numeric import IntegerField

from model.order import Order, OrderDetail, Pallet


class OrderDetailForm(FlaskForm):
    product_id = StringField('商品编号')
    product_model = StringField('商品型号')
    qty = IntegerField('数量')
    type = StringField('类型')
    unit_price = FloatField('单价')
    ctns = IntegerField('集装箱')
    total_price = FloatField('总价')
    nw_kgs = FloatField('净重')  # 根据数据和商品的净重计算出来的
    gw_kgs = FloatField('毛重')  # 根据数据和商品的净重计算出来的
    mt_cmb = FloatField('体积')  # 根据数据和商品的体积计算出来的


class PalletForm(FlaskForm):
    width = FloatField('宽')
    height = FloatField('高')
    length = FloatField('长')
    nw_kgs = FloatField('净重')
    gw_kgs = FloatField('毛重')
    mt_cmb = FloatField('体积')
    qty = IntegerField('数量')
    total_mt_cmb = FloatField('总体积')
    total_nw_kgs = FloatField('总净重')
    total_gw_kgs = FloatField('总毛重')


class OrderForm(FlaskForm):
    po_num = StringField('订单编号')
    customer_id = StringField('客户编号')
    pi_num = StringField('PI编号')
    po_date = DateField('订单日期', format='%Y-%m-%d')
    payment_method = StringField('付款方式')
    delivery_date = DateField('交货日期', format='%Y-%m-%d')
    port_of_loading = StringField('装运港')
    port_of_destination = StringField('目的港')
    ctn_size_qty = FloatField('集装箱尺寸')
    billing_of_loading_num = StringField('装运单号')
    ctn_num = StringField('集装箱号')
    seal_num = StringField('铅封号')
    lot = DateField('LOT日期')
    workshop = StringField('车间名')
    batch_num = StringField('批次号')
    remarks = TextAreaField('备注')
    order_details = FieldList(FormField(OrderDetailForm))
    part_details = FieldList(FormField(OrderDetailForm))
    pallets = FieldList(FormField(PalletForm))

    @staticmethod
    def build_form(order) -> 'OrderForm':
        form = OrderForm()
        for field in form:
            if hasattr(order, field.name):
                field.data = getattr(order, field.name)

        order_details = []
        for detail in order.order_details:
            detail_form = OrderDetailForm()
            for field in detail_form:
                if hasattr(detail, field.name):
                    field.data = getattr(detail, field.name)
            order_details.append(detail_form)
        form.order_details = order_details

        part_details = []
        for detail in order.part_details:
            detail_form = OrderDetailForm()
            for field in detail_form:
                if hasattr(detail, field.name):
                    field.data = getattr(detail, field.name)
            part_details.append(detail_form)
        form.part_details = part_details

        pallets = []
        for pallet in order.pallets:
            pallet_form = PalletForm()
            for field in pallet_form:
                if hasattr(pallet, field.name):
                    field.data = getattr(pallet, field.name)
            pallets.append(pallet_form)
        form.pallets = pallets
        return form

    def build_order(self) -> Order:
        order = Order()
        for field in self:
            if hasattr(order, field.name):
                setattr(order, field.name, field.data)
        order_details = []
        for detail_form in self.order_details:
            order_detail = OrderDetail()
            order_detail.type = '商品'
            for field in detail_form:
                if hasattr(order_detail, field.name):
                    setattr(order_detail, field.name, field.data)
            order_details.append(order_detail)
        order.order_details = order_details

        part_details = []
        for detail_form in self.part_details:
            order_detail = OrderDetail()
            order_detail.type = '配件'
            for field in detail_form:
                if hasattr(order_detail, field.name):
                    setattr(order_detail, field.name, field.data)
            part_details.append(order_detail)
        order.part_details = part_details

        pallets = []
        for pallet_form in self.pallets:
            pallet = Pallet()
            for field in pallet_form:
                if hasattr(pallet, field.name):
                    setattr(pallet, field.name, field.data)
            pallets.append(pallet)
        order.pallets = pallets
        return order
