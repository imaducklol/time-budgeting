"""
Author:  Orion Hess
Created: 2025-12-09
Edited:  2025-12-11

Routes for category management
"""

from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Category
from datetime import timedelta

category_bp = Blueprint('categories', __name__)

@category_bp.get('')
def get_categories(user_id, budget_id):
    detailed = request.args.get('detailed', 'false').lower() == 'true'
    categories = Category.query.filter(Category.budget_id == budget_id).all()
    if detailed:
        print("called detailed")
        return jsonify([category.to_dict_with_transactions() for category in categories]), 200
    else:
        return jsonify([category.to_dict() for category in categories]), 200

@category_bp.post('')
def create_category(user_id, budget_id):
    data = request.get_json()

    if not data.get('category_name') or not data.get('time_allocated'):
        return jsonify({'error': 'Category name and time allocated are required.'}), 400

    category = Category(
        category_name=data.get('category_name'),
        time_allocated=timedelta(seconds=data.get('time_allocated')),
        group_id=data.get('group_id'),
        budget_id=budget_id
    )

    db.session.add(category)
    db.session.commit()

    return jsonify(category.to_dict()), 201

@category_bp.get('/<int:category_id>')
def get_category(user_id, budget_id, category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_dict()), 200

@category_bp.patch('/<int:category_id>')
def update_category(user_id, budget_id, category_id):
    data = request.get_json()
    if not data or not data.get("category_name") or not data.get("time_allocated"):
        return jsonify({'error': 'Category name and time allocated are required'}), 400

    category = Category.query.filter(Category.category_id == category_id).first()
    if category is None:
        return jsonify({'error': 'Category not found'}), 404

    category.category_name = data.get("category_name")
    category.time_allocated = timedelta(data.get("time_allocated"))

    db.session.commit()

    return jsonify(category.to_dict()), 201

@category_bp.delete('/<int:category_id>')
def delete_category(user_id, budget_id, category_id):
    category = Category.query.filter(Category.category_id == category_id).first()

    if category is None:
        return jsonify({'error': 'Category not found'}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({'message': 'Category deleted'}), 200
