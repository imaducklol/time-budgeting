"""
Author:  Orion Hess
Created: 2025-12-09
Edited:  2025-12-09

Routes for group management
"""

from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Group, Category

group_bp = Blueprint('groups', __name__)

@group_bp.get('')
def get_groups(user_id, budget_id):
    groups = Group.query.filter(Group.budget_id == budget_id).all()
    return jsonify([group.to_dict() for group in groups]), 200

@group_bp.post('')
def create_group(user_id, budget_id):
    data = request.get_json()

    if not data.get('group_name'):
        return jsonify({'error': 'Group name not provided.'}), 400

    group = Group(
        group_name=data.get('group_name'),
        budget_id=budget_id
    )

    db.session.add(group)
    db.session.commit()

    return jsonify(group.to_dict()), 201

@group_bp.get('/<int:group_id>')
def get_group(user_id, budget_id, group_id):
    group = Group.query.get_or_404(group_id)
    return jsonify(group.to_dict()), 200

@group_bp.patch('/<int:group_id>')
def update_group(user_id, budget_id, group_id):
    data = request.get_json()
    if not data or not data.get("group_name"):
        return jsonify({'error': 'Group name is required.'}), 400

    group = Group.query.filter(Group.group_id == group_id).first()
    if group is None:
        return jsonify({'error': 'Group not found.'}), 404

    group.group_name = data.get('group_name')

    db.session.commit()

    return jsonify(group.to_dict()), 201

@group_bp.delete('/<int:group_id>')
def delete_group(user_id, budget_id, group_id):
    group = Group.query.filter(Group.group_id == group_id).first()

    if group is None:
        return jsonify({'error': 'Group not found.'}), 404

    db.session.delete(group)
    db.session.commit()

    return jsonify({'message': 'Group deleted.'}), 200

@group_bp.get('/<int:group_id>/categories')
def get_group_categories(user_id, budget_id, group_id):
    detailed = request.args.get('detailed', 'false').lower() == 'true'
    categories = Category.query.filter(Category.budget_id == budget_id, Category.group_id == group_id).all()
    if detailed:
        return jsonify([category.to_dict_with_transactions() for category in categories]), 200
    else:
        return jsonify([category.to_dict() for category in categories]), 200