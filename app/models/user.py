from flask_login import UserMixin
import time

from app.core.db import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.Integer, default=int(time.time()), nullable=False)
    updated_at = db.Column(db.Integer, default=int(time.time()), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)