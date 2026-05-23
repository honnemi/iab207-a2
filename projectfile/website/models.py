from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    comments = db.relationship('Comment', backref='user', lazy=True)
    orders = db.relationship('Booking', backref='user', lazy=True)
    events = db.relationship('Event', backref = 'owner', lazy=True)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(50))
    rating = db.Column(db.String(10))
    ticket_price = db.Column(db.Float)
    tickets_available = db.Column(db.Integer)
    location = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime)
    image = db.Column(db.String(255))

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)
    is_cancelled = db.Column (db.Boolean, default = False, nullable=False)
    acknowledgment_type = db.Column(db.String(20), default='none', nullable=False)
    acknowledgement_text = db.Column(db.Text, nullable=True)

    comments = db.relationship('Comment', backref='event', lazy=True)
    orders = db.relationship('Booking', backref='event', lazy=True)

    @property
    def status(self):
        """ Auto - computed - never stored in DB."""
        if self.is_cancelled:
            return 'Cancelled'
        if self.tickets_available is not None and self.tickets_available <= 0:
            return 'Sold Out'
        if self.date and self.date < datetime.now(datetime.timezone.utc):
            return 'Inactive'
        return 'Open'
    

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)


class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)