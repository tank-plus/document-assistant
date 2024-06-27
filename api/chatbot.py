from flask_restx import Namespace, Resource, fields
from core.util import *
from flask import request

chatbot_ns = Namespace('chatbot', description='chatbot related operations')


chat_model = chatbot_ns.model('Chat', {
   'message': fields.String(required=True, description='The message to be processed by the chatbot', example='我要创建一个新的订单')
})


@chatbot_ns.route('/process')
class Chatbot(Resource):
    
    @chatbot_ns.doc('process')
    @chatbot_ns.expect(chat_model)
    @wrap_response
    def post(self):
        # TODO: process the chatbot request and return the response
        message = request.json.get('message')
        
        # 我要创建一个新的订单 -> 弹出订单创建对话框
        if message == '我要创建一个新的订单':
            return "请问需要什么样的订单？"
        
        # 帮我复制订单ou12345678创建一个新的订单 -> 复制订单内容并弹出订单创建对话框
        if message.startswith('帮我复制订单'):
            order_id = message.split(' ')[-1]
            return f"请问需要什么样的订单？订单号为{order_id}的订单已经复制成功，请修改订单信息后提交。"
        
        # 帮我查下未确认的订单列表 -> 展示未确认的订单表格
        if message == '帮我查下未确认的订单列表':
            return "您有以下未确认的订单：\n订单1号，订单2号，订单3号。"
        
        # 我要预览订单ou12345678 -> 表格展示订单的pi信息
        if message.startswith('我要预览订单'):
            order_id = message.split(' ')[-1]
            return f"订单号为{order_id}的订单预览如下：\n商品名称：苹果手机\n商品价格：1999元\n商品数量：1\n收件人：张三\n收件地址：北京市海淀区西二旗北路10号"
        
        # 帮我确认订单ou12345678,ou98123456 -> 订单状态改为已确认，生成订单确认附件excel
        if message.startswith('帮我确认订单'):
            order_ids = message.split(' ')[-1].split(',')
            return f"已确认订单号为{order_ids}的订单。"
        
        # 帮我列下已经确认的订单列表 -> 展示近3月已经确认的订单表格？
        if message == '帮我列下已经确认的订单列表':
            return "您有以下已经确认的订单：\n订单1号，订单2号，订单3号。"
        
        # 帮我将订单ou12345678,ou7890123123合并进行商检 -> 提示商检单创建成功，可以进行预览确认，相关订单状态改为商检中
        if message.startswith('帮我将订单'):
            order_ids = message.split(' ')[-1].split(',')
            return f"已将订单号为{order_ids}的订单合并进行商检。"
        
        # 我要预览商检单po12345678 -> 表格展示商检单的pi ci pl信息
        if message.startswith('我要预览商检单'):
            order_id = message.split(' ')[-1]
            return f"商检单号为{order_id}的商检单预览如下：\n商品名称：苹果手机\n商品价格：1999元\n商品数量：1\n收件人：张三\n收件地址：北京市海淀区西二旗北路10号"
        
        # 帮我确认商检单po12345678 -> 商检单状态改为已商检，生成商检单确认附件excel，相关ysql订单状态改为已商检
        if message.startswith('帮我确认商检单'):
            order_id = message.split(' ')[-1]
            return f"已确认商检单号为{order_id}的商检单。"
        
        
        # 帮我将商检单po123134转为报关单 -> 商检单状态改为报关中，输入提运单号，相关订单状态改为报关中
        if message.startswith('帮我将商检单'):
            order_id = message.split(' ')[-1]
            
            return f"已将商检单号为{order_id}的商检单转为报关单。"
        
        # 我要预览报关单po12345678 -> 表格展示报关单的pi ci pl信息
        if message.startswith('我要预览报关单'):
            order_id = message.split(' ')[-1]
            return f"报关单号为{order_id}的报关单预览如下：\n商品名称：苹果手机\n商品价格：1999元\n商品数量：1\n收件人：张三\n收件地址：北京市海淀区西二旗北路10号"
        
        # 帮我确认报关单po12345678 -> 订单状态改为已报关，生成报关单确认附件excel，相关订单状态改为已报关
        if message.startswith('帮我确认报关单'):
            order_id = message.split(' ')[-1]
            return f"已确认报关单号为{order_id}的报关单。"
        
        # 帮我将报关单po12345678,po7890123123合并进行清关 -> 提示清关单创建成功，可以进行预览确认，相关订单状态改为清关中
        if message.startswith('帮我将报关单'):
            order_ids = message.split(' ')[-1].split(',')
            return f"已将报关单号为{order_ids}的报关单合并进行清关。"
        
        # 我要预览清关单po12345678 -> 表格展示清关单的pi ci pl信息
        if message.startswith('我要预览清关单'):
            order_id = message.split(' ')[-1]
            return f"清关单号为{order_id}的清关单预览如下：\n商品名称：苹果手机\n商品价格：1999元\n商品数量：1\n收件人：张三\n收件地址：北京市海淀区西二旗北路10号"
        
        # 帮我确认清关单po12345678 -> 清关单状态改为已清关，生成清关单确认附件excel，相关订单状态改为已清关
        if message.startswith('帮我确认清关单'):
            order_id = message.split(' ')[-1]
            return f"已确认清关单号为{order_id}的清关单。"
        
        
        
        