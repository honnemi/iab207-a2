
from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin): 
    pass

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    location = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    image = db.Column(db.String(255))

class Comment(db.Model):
    pass

class Order(db.Model): 
    pass
