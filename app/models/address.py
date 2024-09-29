
from app.core.db import db
import time

class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    favorite = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.Integer, default=int(time.time()), nullable=False)
    updated_at = db.Column(db.Integer, default=int(time.time()), nullable=False)

    user = db.relationship('User', backref=db.backref('addresses', lazy=True))
