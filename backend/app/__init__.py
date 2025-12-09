"""
Author:  Orion Hess
Created: 2025-12-03
Edited:  2025-12-03

Module to serve endpoints for our database
"""

from flask import Flask
from app.config import Config
from app.database import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)

    from app.routes.users import user_bp
    from app.routes.budgets import budget_bp
    from app.routes.groups import group_bp
    from app.routes.categories import category_bp
    from app.routes.transactions import transaction_bp
    app.register_blueprint(user_bp)
    user_bp.register_blueprint(budget_bp, url_prefix='/<int:user_id>/budgets')
    budget_bp.register_blueprint(group_bp, url_prefix='/<int:group_id>/groups')
    budget_bp.register_blueprint(category_bp, url_prefix='/<int:category_id>/categories')
    category_bp.register_blueprint(transaction_bp, url_prefix='/<int:transaction_id>/transactions')

    # Create tables that do not exist yet
    with app.app_context():
        db.create_all()

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app
