# Define a template for CRUD operations

from model.user import User
from jinja2 import Environment, DictLoader

view_template = """
from flask import Blueprint, render_template, request, redirect, url_for
from model.{entity_name_lower} import {entity_name}
from model.db import db
from route.common import login_required
{entity_name_lower}_bp = Blueprint('{entity_name_lower}', __name__)

@{entity_name_lower}_bp.route('/')
@login_required
def {entity_name_lower}_list():
    items = {entity_name}.query.all()
    return render_template('{entity_name_lower}.html', items=items)

@{entity_name_lower}_bp.route('/add')
@login_required
def {entity_name_lower}_add():
    return render_template('{entity_name_lower}_edit.html')
    
    
@{entity_name_lower}_bp.route('/save', methods=['POST'])
@login_required
def {entity_name_lower}_save():
    return redirect(url_for('{entity_name_lower}.{entity_name_lower}'))
    
    
@{entity_name_lower}_bp.route('/delete/<id>')
@login_required
def {entity_name_lower}_delete(id):
    return redirect(url_for('{entity_name_lower}.{entity_name_lower}'))
"""

# Assuming we can somehow loop through or dynamically load entities
entities = [User]  # This could be a list of entities, dynamically loaded
module_name = "用户"

for entity in entities:
    entity_name = entity.__name__
    # Add logic to convert entity fields into route and template logic
    # Generate Flask views based on the template and save them to a file
    with open(f"route/{entity_name.lower()}.py", "w", encoding="utf-8") as f:
        f.write(view_template.format(entity_name=entity_name, entity_name_lower=entity_name.lower()))
        
        
list_page = """
{% raw %}
{% extends 'base.html' %}

{% block content %}
{% endraw %}
<!-- Content Header (Page header) -->
<section class="content-header">
    <div class="container-fluid">
        <div class="row mb-2">
            <div class="col-sm-6">
                <h1>{{ module_name }}管理</h1>
            </div>
        </div>
    </div><!-- /.container-fluid -->
</section>

<section class="content">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">

                <div class="callout callout-info" style="font-size: 12px;">
                    <h5><i class="fas fa-info"></i> Note:</h5>
                    客户存在多个收货地址，商检和报关时需要用实际收货地址，订单确认和国外清关时用总部地址
                </div>

                <div class="card">
                    <!-- /.card-header -->
                    <div class="card-body p-0">
                        <p style="padding: 20px 0px 0px 20px;">
                            <a href="/{{entity_name_lower}}/add" class="btn btn-default btn-sm" style="font-size: 12px;">新建{{ module_name }}</a>
                        </p>
                        <table class="table table-bordered" style="font-size: 12px;">
                            <thead>
                                <tr>
                                    <th>客户名称</th>
                                    <th>客户别名</th>
                                    <th>名称缩写</th>
                                    <th>总部地址</th>
                                    <th>国家</th>
                                    <th>国家缩写</th>
                                    <th>收货地址</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                
                            </tbody>
                        </table>
                    </div>
                    <!-- /.card-body -->
                </div>
                <!-- /.card -->
            </div>

        </div>
    </div>
</section>

<script>
    $(".record-delete").click(function() {
        var id = $(this).data("id");
        $("#btn-confirm-delete").data("id", id);
        $("#modal-default").modal("show");
    });
</script>
<div class="modal fade" id="modal-default">
    <div class="modal-dialog">
        <div class="modal-content">
        <div class="modal-header ">
            <h4 class="modal-title">消息提示</h4>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <form id="delete-form" method="POST">
                <p>确认删除{{ module_name }}?</p>
            </form>
        </div>
        <div class="modal-footer justify-content-between">
            <button type="button" class="btn btn-default btn-sm" data-dismiss="modal">取消</button>
            <button type="button" class="btn btn-danger btn-sm" id="btn-confirm-delete">确认</button>
            <script>
                $("#btn-confirm-delete").click(function() {
                    var id = $(this).data("id");
                    $("#delete-form").attr("action", "/{{entity_name_lower}}/delete/" + id);
                    $("#delete-form").submit();
                    $("#modal-default").modal("hide");
                });
            </script>
        </div>
        </div>
        <!-- /.modal-content -->
    </div>
<!-- /.modal-dialog -->
</div>
<!-- /.modal -->
{% raw %}
{% endblock %}
{% endraw %}
"""


edit_page= """
{% raw %}
{% extends 'base.html' %}

{% block content %}
{% endraw %}
<section class="content-header">
    <div class="container-fluid">
        <div class="row mb-2">
            <div class="col-sm-6">
                <h1>新建{{ module_name }}</h1>
            </div>
        </div>
    </div><!-- /.container-fluid -->
</section>

<section class="content">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">


                <div class="card">
                    <!-- /.card-header -->
                    <div class="card-body p-0">
                        <div class="card-body">
                            <form action="/{{entity_name_lower}}/save" method="post">
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-md-4">
                                            <input class="form-control form-control-sm" type="text" placeholder="客户名称" name="customer_id" required/>
                                        </div>
                                        <div class="col-md-4">
                                            <input class="form-control form-control-sm" type="text" placeholder="客户别名" name="alias_name" required/>
                                        </div>
                                        <div class="col-md-4">
                                            <input class="form-control form-control-sm" type="text" placeholder="名称缩写" name="short_name" required/>
                                        </div>
                                    </div>
                                    
                                </div>
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-md-4">
                                            <input class="form-control form-control-sm" type="text" placeholder="国家" name="country" required/>
                                        </div>
                                        <div class="col-md-4">
                                            <input class="form-control form-control-sm" type="text" placeholder="国家缩写" name="country_short_name" required/>
                                        </div>
                                        <div class="col-md-4">
                                            <input class="form-control form-control-sm" type="text" placeholder="Tel/Fax" name="tel_fax"/>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-md-12">
                                            <input class="form-control form-control-sm" type="text" placeholder="总部地址" name="address" required/>
                                        </div>
                                    </div>   
                                </div>
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-md-12">
                                            <textarea class="form-control" rows="3" placeholder="备注" name="remarks"></textarea>
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-sm-4"><h5 style="display: inline;">收货地址</h5> <button type="button" class="btn btn-default btn-sm"><i class="fa fa-plus"></i> 新增收货地址</button></div>
                                
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-md-2">
                                            <input class="form-control form-control-sm" type="text" placeholder="收货地名称"/>
                                        </div>
                                        <div class="col-md-6">
                                            <input class="form-control form-control-sm" type="text" placeholder="收货地址"/>
                                        </div>
                                        <div class="col-md-3">
                                            <input class="form-control form-control-sm" type="text" placeholder="Tel/Fax"/> 
                                        </div>
                                        <div class="col-md-1">
                                            <button type="button" class="btn btn-default btn-sm"><i class="fa fa-trash"></i></button>
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-md-2">
                                            <input class="form-control form-control-sm" type="text" placeholder="收货地名称"/>
                                        </div>
                                        <div class="col-md-6">
                                            <input class="form-control form-control-sm" type="text" placeholder="收货地址"/>
                                        </div>
                                        <div class="col-md-3">
                                            <input class="form-control form-control-sm" type="text" placeholder="Tel/Fax"/>
                                        </div>
                                        <div class="col-md-1">
                                            <button type="button" class="btn btn-default btn-sm"><i class="fa fa-trash"></i></button>
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-md-12">
                                            <button type="submit" class="btn btn-primary btn-sm">确认</button>
                                            <a href="javascript:window.history.back()" class="btn btn-default btn-sm" style="margin-right: 5px;">取消</a>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>

                    </div>
                    <!-- /.card-body -->
                </div>
                <!-- /.card -->
            </div>

        </div>
    </div>
</section>
{% raw %}
{% endblock %}
{% endraw %}
"""
template_dict = {
    'list_page_template': list_page,
    'edit_page_template': edit_page
}

# 创建环境
env = Environment(loader=DictLoader(template_dict))

# Again, loop through entities
for entity in entities:
    # Dynamically generate the listing page based on the entity fields
    with open(f"templates/{entity.__name__.lower()}.html", "w", encoding="utf-8") as f:
        f.write(env.get_template('list_page_template').render(entity_name=entity.__name__, entity_name_lower=entity.__name__.lower(), module_name=module_name))
        
    with open(f"templates/{entity.__name__.lower()}_edit.html", "w", encoding="utf-8") as f:
        f.write(env.get_template('edit_page_template').render(entity_name=entity.__name__, entity_name_lower=entity.__name__.lower(), module_name=module_name))