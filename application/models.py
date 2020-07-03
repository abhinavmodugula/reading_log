# -*- coding: utf-8 -*-
"""
Database Models

@author: abhin
"""

from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User account model."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),index=True, nullable=False,unique=True)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    created_on = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    admin = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    recieve_recs = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    email = db.Column(db.String(100), primary_key=False, unique=True, nullable=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True, nullable=False, unique=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, index=True)
    user = relationship("User", backref="categories", foreign_keys=[user_id])

class Book(db.Model):
    """ Table for the books a user keeps track of privately. """
    __tablename__ = 'books_and_other_readings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), index=True, unique=True, nullable=False)
    author = db.Column(db.String(80), index=False, unique=False, nullable=True)
    date_started = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    description = db.Column(db.Text, index=False, unique=False, nullable=True)
    complete = db.Column(db.Boolean, index=False, unique=False, nullable=True)
    
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, index=True)
    user = relationship("User", backref = "books", foreign_keys=[user_id])
    cat_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=True, index=True)
    category = relationship("Category", backref="books", foreign_keys=[cat_id])

class BookUpdate(db.Model):
    """ Table for updates to the book. """
    __tablename__ = 'book_updates'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    pages = db.Column(db.String(100), index=False, unique=False, nullable=True)
    text = db.Column(db.Text, index=False, unique=False, nullable=False)
    
    book_id = db.Column(db.Integer, ForeignKey('books_and_other_readings.id'), nullable=False, index=True)
    book = relationship("Book", backref = "book_updates", foreign_keys=[book_id])
    
    
class PublicPost(db.Model):
    __tablename__ = "public_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    text = db.Column(db.Text, index=False, unique=False, nullable=False)
    likes = db.Column(db.Integer, index=False, unique=False, nullable=True)
    dislikes = db.Column(db.Integer, index=False, unique=False, nullable=True)

    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, index=True)
    user = relationship("User", backref = "public_posts", foreign_keys=[user_id])


class PublicReply(db.Model):
    __tablename__ = "publicreplys"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    text = db.Column(db.Text, index=False, unique=False, nullable=False)
    
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, index=True)
    user = relationship("User", backref = "public_replys", foreign_keys=[user_id])
    post_id = db.Column(db.Integer, ForeignKey('public_posts.id'), nullable=False, index=True)
    post = relationship("PublicPost", backref="replys", foreign_keys=[post_id])
    

