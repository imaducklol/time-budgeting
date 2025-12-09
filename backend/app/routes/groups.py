from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Group

group_bp = Blueprint('groups', __name__)

@group_bp.get('')
def get_budgets(user_id, budget_id):
    groups = Group.query.filter(Group.budget_id == budget_id).all()
    return jsonify([group.to_dict() for group in groups]), 200

@group_bp.post('')
def create_budget(user_id, budget_id):
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
def get_budget(user_id, budget_id, group_id):
    group = Group.query.get_or_404(group_id)
    return jsonify(group.to_dict()), 200

@group_bp.patch('/<int:group_id>')
def update_budget(user_id, budget_id, group_id):
    pass

@group_bp.delete('/<int:group_id>')
def delete_budget(user_id, budget_id, group_id):
    pass
