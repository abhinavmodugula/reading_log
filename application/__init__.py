# -*- coding: utf-8 -*-
"""
Creates the app

@author: abhin
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "dsahiash7897hhdkjh12"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        from . import routes
        from . import auth
        from .models import User, Book, BookUpdate, PublicPost
        
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(routes.main_bp)
        db.create_all()
        
        return app
