"""
Author: Orion Hess
Created: 2025-12-03
Updated: 2025-12-03

Configuration settings for the time budgeting application.
"""

import os
import dotenv

dotenv.load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-standin-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False