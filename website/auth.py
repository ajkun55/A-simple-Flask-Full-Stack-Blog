from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrect', category='error')
        else:
            flash('User not exist', category='error')
            
    return render_template("login.html", user = current_user)

@auth.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':        
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already in use', category='error')
        elif username_exists:
            flash('Username is already in use', category='error')
        elif password != password2:
            flash("Password don't match", category='error')
        elif len(username) < 2:
            flash("Username should have more characters", category='error')
        elif len(password) < 6:
            flash("Password should have more characters", category='error')
        elif len(email) < 4:
            flash("Email should have more characters", category='error')
        else:
            new_user = User(email=email, username=username, password = generate_password_hash(password, method='pbkdf2'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User created!")
            return redirect(url_for('views.home'))


    return render_template("signup.html", user = current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))