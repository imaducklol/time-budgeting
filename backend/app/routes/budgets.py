"""
Author:  Orion Hess
Created: 2025-12-09
Edited:  2025-12-09

Routes for budget management
"""

from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Budget

budget_bp = Blueprint('budgets', __name__)

@budget_bp.get('')
def get_budgets(user_id):
    budgets = Budget.query.filter(Budget.user_id == user_id).all()
    return jsonify([budget.to_dict() for budget in budgets]), 200

@budget_bp.post('')
def create_budget(user_id):
    data = request.get_json()

    if not data.get('budget_name'):
        return jsonify({'error': 'Budget name not provided.'}), 400

    budget = Budget(
        budget_name=data.get('budget_name'),
        user_id=user_id
    )

    db.session.add(budget)
    db.session.commit()

    return jsonify(budget.to_dict()), 201

@budget_bp.get('/<int:budget_id>')
def get_budget(user_id, budget_id):
    budget = Budget.query.get_or_404(budget_id)
    return jsonify(budget.to_dict()), 200

@budget_bp.patch('/<int:budget_id>')
def update_budget(user_id, budget_id):
    pass

@budget_bp.delete('/<int:budget_id>')
def delete_budget(user_id, budget_id):
    pass