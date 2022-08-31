from FET_user import User
from FET_user import db
from SR_db import SR
from SR_db import sr_db
from SR_ad import AD
from SR_ad import ad_db
from flask import Flask, render_template, request, session
from flask_paginate import Pagination, get_page_args
from sqlalchemy import or_
import pandas as pd
import pandas, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from datetime import date
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import request, render_template, url_for, redirect,url_for
from flask import request, render_template, url_for, redirect, flash
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請證明你並非來自黑暗草泥馬界'
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(使用者):
    if 使用者 not in users:
        return

    user = User()
    user.id = 使用者
    return user

@login_manager.request_loader
def request_loader(request):
    使用者 = request.form.get('user_id')
    if 使用者 not in users:
        return

    user = User()
    user.id = 使用者

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[使用者]['password']

    return user

users = {'Me': {'password': 'myself'}}
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    使用者 = request.form['user_id']
    if (使用者 in users) and (request.form['password'] == users[使用者]['password']):
        user = User()
        user.id = 使用者
        login_user(user)
        flash(f'{使用者}！歡迎加入草泥馬訓練家的行列！')
        return redirect(url_for('from_start'))

    flash('登入失敗了...')
    return render_template('login.html')
@app.route('/logout')
def logout():
    使用者 = current_user.get_id()
    logout_user()
    flash(f'{使用者}！歡迎下次再來！')
    return render_template('login.html')
@app.route("/show_records")
@login_required
def show_records():
    python_records =web_select_overall()
    return render_template("show_records.html", html_records=python_records)
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5008, debug=True)