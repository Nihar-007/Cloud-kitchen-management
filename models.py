from __main__ import db
from datetime import datetime

class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phno = db.Column(db.Integer(), unique=True, nullable=False)
    passwd = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(50), default='customer')

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(30), nullable=False)
    item = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    image = db.Column(db.String(30), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    message = db.Column(db.Text, nullable=False)

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    offer_on = db.Column(db.String(100), nullable=False) 
    start = db.Column(db.Date, nullable=False, default=datetime.now)
    valid = db.Column(db.Date, nullable=False)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(20), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
class Order_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    items = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.String(70), nullable=False)
    amount = db.Column(db.String(70), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    datee = db.Column(db.Date, nullable=False, default=datetime.now)
    
class Ip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipv4 = db.Column(db.String(50), nullable=False)
    ipv6 = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    isp = db.Column(db.String(100), nullable=False)

class Order_pending(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    items = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    datee = db.Column(db.Date, nullable=True)