# -*- coding: utf-8 -*-
"""
User routes for login and signup.
Can easily be used in other apps.

@author: abhin
"""
import functools
from datetime import datetime
from .models import db, User
from flask import render_template, request, flash, redirect, url_for, Blueprint, session, g

#Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    """
    GET: Login form
    POST: Logins in a user and redirects to mylog

    """

    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['uname']).first()  # Validate Login Attempt
        if user and user.check_password(password=request.form['pswd']):
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main_bp.myLog'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template("login.html", user="None")

@auth_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    """
    Creates new users
    GET: Serves the sign up page
    POST: Creates new user and redirects to MyLog Home
    
    """
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pswd']
        email = request.form["e-mail"]
        notifications = request.form.get("notif")
        
        existing_user = User.query.filter_by(name=request.form['uname']).first()

        if existing_user is not None:
            flash("A user with that username already exists please enter a new one.")
        else:
            if notifications:
                new_user = User(name=username, email=email, admin=False, recieve_recs=False, created_on=datetime.now())
            else:
                new_user = User(name=username, admin=False, recieve_recs=False, created_on=datetime.now())
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            session.clear()
            session['user_id'] = new_user.id
            return redirect(url_for('main_bp.myLog'))

    return render_template("signup.html", user="None")

@auth_bp.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("main_bp.hello"))

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth_bp.login'))

        return view(**kwargs)

    return wrapped_view


