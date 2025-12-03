from app.database import db
from datetime import datetime

"""
Objects:
    user(user_id, username, email)
    device(user_id, name) 
        uid -> user(name) cascade
    budget(budget_id, budget_name, user_id)
        user_id -> user(user_id)
    category(category_id, category_name, time_allocated, budget_id, group_id)
        budget_id -> budget(budget_id)
        group_id -> group(group_id) - nullable
    group(group_id, group_name, budget_id)
        budget_id -> budget(budget_id)
    transaction(transaction_id, transaction_name, period, date_time, from?, category_id)
        category_id -> category(category_id)
    
    notification()

Relations:
    authorizes(authorizer, authorized)
        authorizer -> user(user_id)
        authorized -> user(user_id)
"""

class User(db.Model):
    __tablename__ = 'user'

    user_id  = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    username = db.Column(db.String(80),  nullable=False)
    email    = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
        }

class device(db.Model):
    __tablename__ = 'device'

    user_id     = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="CASCADE"), primary_key=True)
    device_name = db.Column(db.String(80), primary_key=True)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'device_name': self.device_name,
        }

class budget(db.Model):
    __tablename__ = 'budget'

    budget_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def to_dict(self):
        return {
            'budget_id': self.budget_id,
            'budget_name': self.budget_name,
            'user_id': self.user_id,
        }

class category(db.Model):
    __tablename__ = 'category'

    category_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name  = db.Column(db.String(80), nullable=False)
    time_allocated = db.Column(db.DateTime, nullable=False)
    budget_id      = db.Column(db.Integer, db.ForeignKey('budget.budget_id'), nullable=False)
    group_id       = db.Column(db.Integer, db.ForeignKey('group.group_id'), nullable=True)

    def to_dict(self):
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'time_allocated': self.time_allocated,
            'budget_id': self.budget_id,
            'group_id': self.group_id,
        }

class group(db.Model):
    __tablename__ = 'group'

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(80), nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.budget_id'), nullable=False)

    def to_dict(self):
        return {
            'group_id': self.group_id,
            'group_name': self.group_name,
            'budget_id': self.budget_id,
        }

class transaction(db.Model):
    __tablename__ = 'transaction'

    transaction_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_name = db.Column(db.String(80), nullable=False)
    period           = db.Column(db.Interval, nullable=False)
    date_time        = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'transaction_name': self.transaction_name,
            'period': self.period,
            'date_time': self.date_time,
        }

class authorizes(db.Model):
    __tablename__ = 'authorizes'

    authorizer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True, nullable=False)
    authorized_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True, nullable=False)

    def to_dict(self):
        return {
            'authorizer_id': self.authorizer_id,
            'authorized_id': self.authorized_id,
        }