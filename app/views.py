from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import UserURL
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', user=current_user)


@views.route('/create_url', methods=['GET', 'POST'])
@login_required
def create_url():
    if request.method == 'POST':
        url = request.form.get('URL')
        short_des = request.form.get('short_des')
        secret_ques = request.form.get('secret_ques')
        secret_ans = request.form.get('secret_ans')
        password = request.form.get('password')

        if len(url) < 1:
            flash('url is too short!', category='error')
        elif len(password) < 1:
            flash('password is too short!', category='error')
        else:
            user_url = UserURL(user_id=current_user.id, url=url, short_des=short_des, secret_ques=secret_ques,
                               secret_ans=secret_ans, password=password, phone=current_user.user_phone_num)
            db.session.add(user_url)
            db.session.commit()
            flash('URL added!', category='success')

    return redirect(url_for('views.profile'))


@views.route('/delete_url/<url_id>', methods=['GET'])
@login_required
def delete_url(url_id):
    user_url = UserURL.query.get(url_id)
    if user_url:
        db.session.delete(user_url)
        db.session.commit()
        flash('URL deleted!', category='success')
    else:
        flash('URL not found!', category='error')
    return redirect(url_for('views.profile'))


@views.route('/delete_url_all/<user_id>', methods=['POST'])
@login_required
def delete_url_all(user_id):
    print('I am here.. ha ha..')
    all_url = UserURL.query.filter_by(user_id=user_id).all()
    print(all_url)
    if all_url:
        for row in all_url:
            url = UserURL.query.filter_by(id=row.id).first()
            print(url)
            if url:
                db.session.delete(url)
                db.session.commit()
        flash('All URL deleted!', category='success')
    else:
        flash('URL not found!', category='error')
    return redirect(url_for('views.profile'))


@views.route('/edit_url/<url_id>', methods=['GET','POST'])
@login_required
def edit_url(url_id):
    user_url = UserURL.query.filter_by(id=url_id).first()

    if user_url:
        if request.method == 'POST':
            url = request.form.get('url')
            short_des = request.form.get('short_des')
            secret_ques = request.form.get('secret_ques')
            secret_ans = request.form.get('secret_ans')
            password = request.form.get('password2')
            if len(url) > 1 and user_url.url != url:
                user_url.url = url
                user_url.modified_by = datetime.now()
            if len(short_des) > 1 and user_url.short_des != short_des:
                user_url.short_des = short_des
                user_url.modified_by = datetime.now()
            if len(secret_ques) > 1 and user_url.secret_ques != secret_ques:
                user_url.secret_ques = secret_ques
                user_url.modified_by = datetime.now()
            if len(secret_ans) > 1 and user_url.secret_ans != secret_ans:
                user_url.secret_ans = secret_ans
                user_url.modified_by = datetime.now()
            if len(password) > 1 and user_url.password != password:
                user_url.password = password
                user_url.modified_by = datetime.now()

            db.session.commit()
            flash('URL updated!', category='success')
            return redirect(url_for('views.profile'))
        else:
            return render_template('edit.html', user=current_user, user_url=user_url)
    else:
        flash('Something error!', category='error')
        return redirect(url_for('views.profile'))



@views.route('/profile', methods=['POST','GET'])
@login_required
def profile():
    return render_template("profile.html", user=current_user, user_url=current_user.user_url)



