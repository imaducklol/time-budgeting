"""
Author:  Orion Hess
Created: 2025-12-03
Edited:  2025-12-11

Routes for user management
"""

from flask import Blueprint, jsonify, request
from app.database import db
from app.models import User

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.get('')
def get_users():
    """Get all users"""
    users = User.query.order_by(User.user_id.desc()).all()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.get('/<int:user_id>')
def get_user(user_id):
    """Get a single user"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

@user_bp.post('')
def create_user():
    """Create a user"""
    data = request.get_json()

    if not data or not data.get("username") or not data.get("email"):
        return jsonify({'error': 'Username and email are required'}), 400

    user = User(
        username=data.get("username"),
        email=data.get("email"),
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201

@user_bp.patch('/<int:user_id>')
def update_user(user_id):
    data = request.get_json()
    if not data or not data.get("username") or not data.get("email"):
        return jsonify({'error': 'Username and email are required'}), 400

    user = User.query.filter(User.user_id == user_id).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    user.username = data.get("username")
    user.email = data.get("email")

    db.session.commit()

    return jsonify(user.to_dict()), 201

@user_bp.delete('/<int:user_id>')
def delete_user(user_id):
    user = User.query.filter(User.user_id == user_id).first()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted'}), 200