"""
Author: Orion Hess
Created: 2025-12-03
Updated: 2025-12-11

Database models for the time budgeting application.
"""

from app.database import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'user'

    user_id  = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    username = db.Column(db.String(80),  nullable=False)
    email    = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime,  nullable=False, server_default=func.now())

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
        }

class Device(db.Model):
    __tablename__ = 'device'

    user_id     = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="CASCADE"), primary_key=True)
    device_name = db.Column(db.String(80), primary_key=True)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'device_name': self.device_name,
        }

class Budget(db.Model):
    __tablename__ = 'budget'

    budget_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            'budget_id': self.budget_id,
            'budget_name': self.budget_name,
            'user_id': self.user_id,
        }

class Category(db.Model):
    __tablename__ = 'category'

    category_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name  = db.Column(db.String(80), nullable=False)
    time_allocated = db.Column(db.Interval, nullable=False)
    budget_id      = db.Column(db.Integer, db.ForeignKey('budget.budget_id', ondelete='CASCADE'), nullable=False)
    group_id       = db.Column(db.Integer, db.ForeignKey('group.group_id'), nullable=True)

    def to_dict(self):
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'time_allocated': self.time_allocated.total_seconds(),
            'budget_id': self.budget_id,
            'group_id': self.group_id,
        }

    def to_dict_with_transactions(self):
        transactions = Transaction.query.filter_by(category_id=self.category_id).all()

        total_seconds = sum(t.period.total_seconds() for t in transactions)

        return_dict = self.to_dict()
        return_dict['time_used'] = total_seconds
        return return_dict

class Group(db.Model):
    __tablename__ = 'group'

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(80), nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.budget_id', ondelete='CASCADE' ), nullable=False)

    def to_dict(self):
        return {
            'group_id': self.group_id,
            'group_name': self.group_name,
            'budget_id': self.budget_id,
        }

class Transaction(db.Model):
    __tablename__ = 'transaction'

    transaction_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_name = db.Column(db.String(80), nullable=False)
    period           = db.Column(db.Interval, nullable=False)
    date_time        = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    category_id      = db.Column(db.Integer, db.ForeignKey('category.category_id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'transaction_name': self.transaction_name,
            'period': self.period.total_seconds(),
            'date_time': self.date_time,
        }

class Authorizes(db.Model):
    __tablename__ = 'authorizes'

    authorizer_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="CASCADE"), primary_key=True, nullable=False)
    authorized_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="CASCADE"), primary_key=True, nullable=False)

    def to_dict(self):
        return {
            'authorizer_id': self.authorizer_id,
            'authorized_id': self.authorized_id,
        }