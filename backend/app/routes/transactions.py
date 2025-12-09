from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Transaction

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.get('')
def get_transactions(user_id, budget_id):
    transactions = Transaction.query.filter(Transaction.budget_id == budget_id).all()
    return jsonify([transaction.to_dict() for transaction in transactions]), 200

@transaction_bp.post('')
def create_transaction(user_id, budget_id):
    data = request.get_json()

    if not data.get('transaction_name'):
        return jsonify({'error': 'Transaction name not provided.'}), 400

    transaction = Transaction(
        group_name=data.get('group_name'),
        budget_id=budget_id
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify(transaction.to_dict()), 201

@transaction_bp.get('/<int:transaction_id>')
def get_transaction(user_id, budget_id, transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    return jsonify(transaction.to_dict()), 200

@transaction_bp.patch('/<int:transaction_id>')
def update_transaction(user_id, budget_id, transaction_id):
    pass

@transaction_bp.delete('/<int:group_id>')
def delete_transaction(user_id, budget_id, transaction_id):
    pass
