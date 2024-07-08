from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, FieldList, FormField, TextAreaField
from wtforms.fields.numeric import IntegerField

from model.order import Order, OrderDetail, Pallet


class OrderDetailForm(FlaskForm):
    pi_category = StringField('PI类别名称')
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
    pallet_name = StringField('名称')
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
    customer_id = IntegerField('客户编号')
    pi_num = StringField('PI编号')
    po_date = DateField('订单日期', format='%Y-%m-%d')
    payment_method = StringField('付款方式')
    delivery_date = StringField('交货日期')
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

    def build_order(self) -> 'Order':
        order = Order(
            po_num=self.po_num.data,
            customer_id=self.customer_id.data,
            pi_num=self.pi_num.data,
            po_date=self.po_date.data,
            payment_method=self.payment_method.data,
            delivery_date=self.delivery_date.data,
            port_of_loading=self.port_of_loading.data,
            port_of_destination=self.port_of_destination.data,
            ctn_size_qty=self.ctn_size_qty.data,
            billing_of_loading_num=self.billing_of_loading_num.data,
            ctn_num=self.ctn_num.data,
            seal_num=self.seal_num.data,
            lot=self.lot.data,
            workshop=self.workshop.data,
            batch_num=self.batch_num.data,
            remarks=self.remarks.data
        )

        order.order_details = []
        for order_detail_form in self.order_details:
            order_detail = OrderDetail(
                pi_category = order_detail_form.pi_category.data,
                order_id=order.po_num,
                product_id=order_detail_form.product_id.data,
                product_model=order_detail_form.product_model.data,
                qty=order_detail_form.qty.data,
                type='商品',
                unit_price=order_detail_form.unit_price.data,
                ctns=order_detail_form.ctns.data,
                total_price=order_detail_form.total_price.data,
                nw_kgs=order_detail_form.nw_kgs.data,
                mt_cmb=order_detail_form.mt_cmb.data,
                gw_kgs=order_detail_form.gw_kgs.data
            )
            order.order_details.append(order_detail)

        order.part_details = []
        for part_detail_form in self.part_details:
            part_detail = OrderDetail(
                pi_category = part_detail_form.pi_category.data,
                order_id=order.po_num,
                product_id=part_detail_form.product_id.data,
                product_model=part_detail_form.product_model.data,
                qty=part_detail_form.qty.data,
                type='配件',
                unit_price=part_detail_form.unit_price.data,
                ctns=part_detail_form.ctns.data,
                total_price=part_detail_form.total_price.data,
                nw_kgs=part_detail_form.nw_kgs.data,
                mt_cmb=part_detail_form.mt_cmb.data,
                gw_kgs=part_detail_form.gw_kgs.data
            )
            order.part_details.append(part_detail)

        order.pallets = []
        for pallet_form in self.pallets:
            pallet = Pallet(
                name = pallet_form.pallet_name.data,
                order_id=order.po_num,
                width=pallet_form.width.data,
                height=pallet_form.height.data,
                length=pallet_form.length.data,
                nw_kgs=pallet_form.nw_kgs.data,
                gw_kgs = pallet_form.gw_kgs.data,
                mt_cmb=pallet_form.mt_cmb.data,
                qty=pallet_form.qty.data,
                total_mt_cmb=pallet_form.qty.data * pallet_form.mt_cmb.data,
                total_nw_kgs=pallet_form.qty.data* pallet_form.nw_kgs.data,
                total_gw_kgs=pallet_form.qty.data* pallet_form.gw_kgs.data
            )
            order.pallets.append(pallet)

        return order
