"""
Author: Orion Hess
Created: 2025-12-03
Updated: 2025-12-10

Entry point for running the Flask application.
"""

from app import create_app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()