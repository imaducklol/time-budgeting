from flask import Blueprint, jsonify, request
from app.database import db
from app.models import User

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.get('')
def get_users():
    """Get all users"""
    users = User.query.all()
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
    # TODO
    pass

@user_bp.delete('/<int:user_id>')
def delete_user(user_id):
    # TODO
    pass