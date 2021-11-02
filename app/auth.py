from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, UserURL
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import string
import random
import requests
from random import *


auth = Blueprint('auth', __name__)


@auth.route('/ran_gen', methods=['GET', 'POST'])
def ran_gen():
    password = 'uyVjOSPBS^3A'
    if request.method == 'GET':
        characters = string.ascii_letters + string.punctuation + string.digits
        password = "".join(choice(characters) for x in range(randint(8, 16)))
    else:
        if request.form.get('first'):
            val = request.form['first']
            if val == 'Enable':
                characters = string.ascii_letters + string.punctuation + string.digits
                password = "".join(choice(characters) for x in range(randint(8, 16)))
                flash('Random Generated Password is ' + password, category='success')
            elif val == 'Disable':
                val2 = "true"
                val1 = "false"
                length = request.form['second1']
                if int(length) < 4:
                    flash('Password Length is too small', category='error')
                    return render_template('pwd_gen.html', user=current_user, password=password)
                else:
                    characters = ''
                    uppercase = lowercase = nums = symbols = ''
                    if request.form.get('second2'):
                        characters += string.ascii_uppercase
                    if request.form.get('second3'):
                        characters += string.ascii_lowercase
                    if request.form.get('second4'):
                        characters += string.digits
                    if request.form.get('second5'):
                        characters += string.punctuation
                    if characters == '':
                        flash('Select minimum one checkbox. Password is random generated', category='error')
                        flash('Random Generated Password is ' + password, category='success')
                    else:
                        password = "".join(choice(characters) for x in range(int(length)))
                        flash('Your Customized Password is ' + password, category='success')
        else:
            flash('Password has been generated random by default. Please select any one radio button', category='error')
            flash('Random Generated Password is ' + password, category='error')
    return render_template('pwd_gen.html', user=current_user, password=password)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email != '':
            if password != '':
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
            else:
                flash('Please enter password', category='error')
        else:
            flash('Enter valid email', category='error')

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
                            if check_password(password2, password1):
                                otp = account_otp_gen(phone)
                                user_details = email+' '+username+' '+password1+' '+phone
                                return render_template("otp_account.html", user=current_user, otp=otp,
                                                       user_details=user_details)
                            else:
                                flash('Passwords don\'t match.', category='error')
                        else:
                            flash('Password must be at least 7 characters.', category='error')

    return render_template("sign_up.html", user=current_user)


def account_otp_gen(phone):
    otp = random.randint(100000, 999999)
    msg = str(otp)
    url = "https://www.fast2sms.com/dev/bulkV2"

    querystring = {"authorization": "SGOeImMlW3JNcRdXY8HAgtrvf4Tz1qVw0ao6ZQpDxys5iCE7PkUQf57MPnY1olHKpgzejvqu2aAmX8Bs",
                   "variables_values": msg, "route": "otp",
                   "numbers": phone}

    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return msg


@auth.route('/create_account/<user>/<otp>', methods=['GET', 'POST'])
def create_account(user, otp):
    entered_otp = request.form.get('otp')
    if entered_otp == otp:
        user_details = list(map(str, user.split(' ')))
        new_user = User(user_email=user_details[0], user_name=user_details[1], user_password=generate_password_hash(
            user_details[2], method='sha256'), user_phone_num=user_details[3])
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Account created!', category='success')
        return redirect(url_for('views.profile'))
    else:
        flash("OTP doesn't match", category='error')
        return render_template("otp_account.html", user=current_user, otp=otp, user_details=user)


@auth.route('/resend_otp/<user>', methods=['GET', 'POST'])
def resend_otp(user):
    user_details = list(map(str, user.split(' ')))
    phone = user_details[3]
    otp = account_otp_gen(phone)
    flash('OTP has been sent again',category='success')
    return render_template("otp_account.html", user=current_user, otp=otp,
                           user_details=user)


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
    num = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}
    if len(phone) != 10:
        flash('phone is not valid.', category='error')
        return 0
    else:
        for i in range(10):
            if phone[i] not in num:
                flash('phone is not valid.', category='error')
                return 0
        return 1



