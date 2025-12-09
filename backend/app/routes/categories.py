from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Category

category_bp = Blueprint('categories', __name__)

@category_bp.get('')
def get_categories(user_id, budget_id):
    categories = Category.query.filter(Category.budget_id == budget_id).all()
    return jsonify([category.to_dict() for category in categories]), 200

@category_bp.post('')
def create_category(user_id, budget_id):
    data = request.get_json()

    if not data.get('category_name') or not data.get('time_allocated'):
        return jsonify({'error': 'Category name and time allocated are required.'}), 400

    category = Category(
        category_name=data.get('category_name'),
        time_allocated=data.get('time_allocated'),
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
    pass

@category_bp.delete('/<int:group_id>')
def delete_category(user_id, budget_id, category_id):
    pass
