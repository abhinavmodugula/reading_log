# -*- coding: utf-8 -*-
"""
Creates the app

@author: abhin
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        from . import routes
        from . import auth
        from .models import User, Book, Category, BookUpdate, PublicPost, PublicReply
        
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(routes.main_bp)
        db.create_all()
        
        return app
