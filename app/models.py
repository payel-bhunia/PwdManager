from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    user_name = db.Column(db.String(20))
    user_email = db.Column(db.String(60))
    user_password = db.Column(db.String(500))
    registration_date = db.Column(db.DateTime, default=datetime.now)
    user_phone_num = db.Column(db.String(19))
    user_url = db.relationship('UserURL')


class UserURL(db.Model):
    __tablename__ = 'userurl'

    id = db.Column(db.Integer, unique=True, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    short_des = db.Column(db.String(100))
    secret_ques = db.Column(db.String(100), nullable=True)
    secret_ans = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.DateTime, default=datetime.now)
    modified_by = db.Column(db.DateTime, nullable=True)
    tier2_auth = db.Column(db.Boolean)
    phone = db.Column(db.String(19))
