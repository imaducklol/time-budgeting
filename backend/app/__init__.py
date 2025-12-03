"""
Author:  Orion Hess
Created: 2025-12-03
Edited:  2025-12-03

Module to serve endpoints for our database
"""

from flask import Flask
from app.config import Config
from app.database import db, init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)


