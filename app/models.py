from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'user' or 'speaker'
    expertise = db.Column(db.String(200))  # Only for speakers
    price_per_session = db.Column(db.Float)  # Only for speakers

    # Relationships
    bookings_as_user = db.relationship('Booking', backref='user', foreign_keys='Booking.user_id', lazy=True)
    bookings_as_speaker = db.relationship('Booking', backref='speaker', foreign_keys='Booking.speaker_id', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)  # e.g., "09:00-10:00"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
