# -*- coding: utf-8 -*-
"""
Routes for the main functionality of the app

@author: abhin
"""

from datetime import datetime
from .models import db, User, Book, BookUpdate, PublicPost
from .auth import login_required
from flask import render_template, request, flash, redirect, url_for, session, g, Blueprint

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route("/")
def hello():
    user = ""
    if g.user is None:
        user = "None"
    return render_template("home.html", user=user)

@main_bp.route("/public")
def all_public_posts():
    posts = PublicPost.query.all()
    user=""
    if g.user is None:
        user = "None"
    return render_template("allpublicposts.html", user=user, posts=posts)

@main_bp.route("/myLog", methods=['GET'])
@login_required
def myLog():
    """
    Shows the user's books and the logs associated with each one'

    """
    user = User.query.filter_by(id=session.get("user_id")).first()
    books = user.books
    return render_template("mylog.html", name=session.get("user_id"), user=user, books=books)

@main_bp.route("/readinglist", methods=['GET'])
@login_required
def reading_list():
    user = User.query.filter_by(id=session.get("user_id")).first()
    books = user.books

    return render_template("readinglist.html", books = books)

@main_bp.route("/publicposts", methods=['GET'])
@login_required
def my_public_posts():
    user = User.query.filter_by(id=session.get("user_id")).first()
    posts = user.public_posts

    return render_template("mypublicposts.html", posts = posts)

@main_bp.route("/create_update111", methods=['POST'])
@login_required
def update():
    title = request.form['title']
    body = request.form['update']
    pages = request.form['pages']
    date = datetime.now()
    book = Book.query.filter_by(id=request.form['book_num']).first()
    new_update = BookUpdate(title=title, date_created=date, text=body, book_id=book.id, book=book, pages=pages)
    db.session.add(new_update)
    db.session.commit()
    return redirect(url_for("main_bp.myLog"))


@main_bp.route("/markcomplete/<int:book_id>")
@login_required
def mark_done(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book is not None:
        book.complete=True
        db.session.commit()
    return redirect(url_for('main_bp.reading_list'))


@main_bp.route("/delete/<int:book_id>")
@login_required
def delete(book_id):
    if book_id is not None:
    	book = Book.query.filter_by(id=book_id).first()
    logs = None
    if book is not None:
        logs = book.book_updates
    if logs is not None:
        for log in logs:
            to_delete = BookUpdate.query.filter_by(id=log.id).first()
            db.session.delete(to_delete)
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('main_bp.reading_list'))

@main_bp.route("/myLog/create_new", methods=['POST', 'GET'])
@login_required
def create_new():
    """
    GET: Returns form to create a new book/article for the current user
    POST: Adds the book/article to the user's table

    """
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        descrp = request.form['descrp']

        book_exists = False
        user = User.query.filter_by(id=session.get("user_id")).first()
        for book in user.books:
            if book.title == title:
                book_exists = True

        if book_exists:
            flash("A book/article with that title has already been created.")
        else:
            new_book = Book(title=title, complete=False, \
                            author=author, description=descrp, date_started=datetime.now(), user=user, \
                                user_id=session.get('session_id'))
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('main_bp.myLog'))
    return render_template("createbook.html")

@main_bp.route("/myLog/create_public_post", methods=['POST', 'GET'])
@login_required
def create_public_post():
    if request.method == 'POST':
        title = request.form['title']
        descrp = request.form['update']

        existing_post = PublicPost.query.filter_by(title=title).first()

        if existing_post is not None:
            flash("A public post with that title has already been created.")
        else:
            user = User.query.filter_by(id=session.get("user_id")).first()
            new_post = PublicPost(title=title, date_created=datetime.now(), user=user, \
                                text = descrp, user_id=session.get('session_id'))
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('main_bp.my_public_posts'))
    return render_template("createpost.html")

@main_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()

