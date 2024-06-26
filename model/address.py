from model.db import db

    
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(4096), unique=False, nullable=False)
    tel_fax = db.Column(db.String(80), unique=False, nullable=True)
    
    def __repr__(self):
        return '<Address %r>' % self.name