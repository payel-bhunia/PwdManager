from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, UserURL
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(user_email=email).first()
        if user:
            if check_password_hash(user.user_password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('name')
        phone = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(user_email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            if check_email_format(email):
                if check_username_format(username):
                    if check_phn(phone):
                        if len(password1) > 7:
                            if check_password(password2,password1):
                                new_user = User(user_email=email, user_name=username, user_password=generate_password_hash(
                                    password1, method='sha256'))
                                db.session.add(new_user)
                                db.session.commit()
                                login_user(new_user, remember=True)
                                flash('Account created!', category='success')
                                return redirect(url_for('views.profile'))
                            else:
                                flash('Passwords don\'t match.', category='error')
                        else:
                            flash('Password must be at least 7 characters.', category='error')

    return render_template("sign_up.html", user=current_user)


def check_email_format(email):
    if len(email) < 5:
        flash('email is too short', category='error')
        return 0
    else:
        if '@' not in email:
            flash('invalid email', category='error')
            return 0
        else:
            return 1


def check_username_format(username):
    if len(username) < 3:
        flash('username must be at least 4 characters.', category='error')
        return 0
    else:
        return 1


def check_password(password2,password1):
    if password1 != password2:
        return 0
    else:
        return 1


def check_phn(phone):
    num = set(1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
    if len(phone) != 10:
        flash('phone is not valid.', category='error')
        return 0
    else:
        for i in range(10):
            if phone[i] not in num:
                flash('phone is not valid.', category='error')
                return 0
        return 1


