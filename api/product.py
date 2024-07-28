from flask_restx import Namespace, Resource, fields
from core.util import *
from flask import request, jsonify
import os
import pandas as pd
import json
from model.product import Product
from model.db import db

product_ns = Namespace('product', description='Product related operations')
upload_parser = product_ns.parser()
upload_parser.add_argument('file', location='files', type='file', required=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ["xlsx","xls"]

@product_ns.route('/upload')
class ProductLoadDataResource(Resource):
    @product_ns.expect(upload_parser)
    def post(self):
        """
        Load product data from file
        """
        if 'file' not in request.files:
            return jsonify({'message': 'No file part in the request'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'})
        if file and allowed_file(file.filename):
            filename = file.filename
            
            if not os.path.exists("./upload"):
                os.makedirs("./upload")
            
            file.save(os.path.join('./upload', filename))
            
            df = pd.read_excel(os.path.join('./upload', filename))
            # table_data = {
            #     "headers": df.columns.tolist(),
            #     "rows": df.values.tolist()
            # }
            # print(table_data)
            # print(json.dumps(table_data,ensure_ascii=False))
            products = []
            for row in df.values.tolist():
                product = Product(
                    id=row[0],
                    model_category=row[1],
                    nw_kgs=row[2],
                    gw_kgs=row[3],
                    length=row[4],
                    width=row[5],
                    height=row[6],
                    mt_cmb = row[7],
                    unit_price=row[8],
                    pcs_cnts_ratio = row[9],
                    pcs_per_cnt = row[10],
                    hs_code = str(row[11]).strip(),
                    hs_us_code = row[12],
                    is_parts = row[13] == "配件",
                    remarks = row[14]
                )
                if not product.query.get(product.id):
                    products.append(product)
            db.session.add_all(products)
            db.session.commit()
            
            # TODO read data from file and save to database
            
            return jsonify({'message': 'File uploaded successfully'})
        else:
            return jsonify({'message': 'Allowed file types are xlsx, xls'}) 