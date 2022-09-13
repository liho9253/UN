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
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
from functools import wraps

app = Flask(__name__)
bcrypt = Bcrypt(app)
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3306/fet"
app.config['SECRET_KEY'] = os.urandom(24)
 
mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'

path_csv = os.path.isfile('order/SR-Sample.csv')
path_excel = os.path.isfile('order/SRTT.xls')
sr_csv = os.path.isfile('order/SR.csv')
ad_csv = os.path.isfile('order/AD.csv')
 
db.init_app(app)
sr_db.init_app(app)
ad_db.init_app(app)

if(path_csv):
    df = pd.read_csv('order/SR-Sample.csv', encoding='big5')
    df.replace("\r\n",'<br>', inplace=True,regex = True)
    df.replace("\n",'<br>', inplace=True,regex = True)
    df.replace("1(High)",'Critical', inplace=True)
    df.replace("2(Medium)",'Major', inplace=True)
    df.replace("3(Low)",'Minor', inplace=True)
    df = df.dropna()
    df = df.drop_duplicates(subset=["SR_ID"], keep="last")
    data_csv = df.to_dict(orient = 'records')
    for row in data_csv:
        row['Major'] = 0
        row['State'] = "In Coming"
        inf = User( row['SR_ID'],
                    row['PLAN_START_DATE_TEXT'],
                    row['PLAN_END_DATE_TEXT'],
                    row['SUBJECT'],
                    row['SPECIALIST_NAME'],
                    row['CREATOR_WORKGROUP_CODE'],
                    row['SR_SUB_CATEGORY'],
                    row['COX_TEXT'],
                    row['CREATOR_NAME'],
                    row['Major'],
                    row['State'])
        if (User.query.filter_by(ID=str(row['SR_ID'])).all() != None):
            inf_db = (User.query.filter_by(ID=str(row['SR_ID'])).all())
            try:
                if inf_db[0].ID != row['SR_ID']:
                    inf_db[0].ID = row['SR_ID']
                if inf_db[0].StartDate != row['PLAN_START_DATE_TEXT']:
                    inf_db[0].StartDate = row['PLAN_START_DATE_TEXT']
                if inf_db[0].EndDate != row['PLAN_END_DATE_TEXT']:
                    inf_db[0].EndDate = row['PLAN_END_DATE_TEXT']
                if inf_db[0].Sub != row['SUBJECT']:
                    inf_db[0].Sub = row['SUBJECT']
                if inf_db[0].SpN != row['SPECIALIST_NAME']:
                    inf_db[0].SpN = row['SPECIALIST_NAME']
                if inf_db[0].CreWGro != row['CREATOR_WORKGROUP_CODE']:
                    inf_db[0].CreWGro = row['CREATOR_WORKGROUP_CODE']
                if inf_db[0].SR != row['SR_SUB_CATEGORY']:
                    inf_db[0].SR = row['SR_SUB_CATEGORY']
                if inf_db[0].CoxT != row['COX_TEXT']:
                    inf_db[0].CoxT = row['COX_TEXT']
                if inf_db[0].CreN != row['CREATOR_NAME']:
                    inf_db[0].CreN = row['CREATOR_NAME']
                if inf_db[0].Major != 0:
                    inf_db[0].Major = inf_db[0].Major
                if inf_db[0].State != "In Coming":
                    inf_db[0].State = inf_db[0].State
                db.session.commit()
            except IndexError:
                db.session.add(inf)
                db.session.commit()
        else:
            db.session.add(inf)
            db.session.commit()
            
if(path_excel):
    df = pandas.read_excel("order/SRTT.xls", usecols=['SR編號', '開始日期', '結束日期', '測試專案名稱', '收單者', '申請部門', '需求分類', '優先順序', 'SR開單者'])
    df.replace("",'', inplace=True,regex = True)
    df = df.dropna()
    data_excel = df.to_dict(orient = 'records')
    for row in data_excel:
        row['Major'] = 0
        row['State'] = "In Coming"
        ssr = row['SR開單者'].split(",")
        row['SR開單者'] = ssr[0]+ssr[1]
        ssr = row['收單者'].split(",")
        row['收單者'] = ssr[0]+ssr[1]
        inf = User( row['SR編號'],
                    row['開始日期'],
                    row['結束日期'],
                    row['測試專案名稱'],
                    row['收單者'],
                    row['申請部門'],
                    row['需求分類'],
                    row['優先順序'],
                    row['SR開單者'],
                    row['Major'],
                    row['State'])
        if (User.query.filter_by(ID=str(row['SR編號'])).all() != None):
            inf_db = User.query.filter_by(ID=str(row['SR編號'])).all()
            try:
                if inf_db[0].ID != row['SR編號']:
                    inf_db[0].ID = row['SR編號']
                if inf_db[0].StartDate != row['開始日期']:
                    inf_db[0].StartDate = row['開始日期']
                if inf_db[0].EndDate != row['結束日期']:
                    inf_db[0].EndDate = row['結束日期']
                if inf_db[0].Sub != row['測試專案名稱']:
                    inf_db[0].Sub = row['測試專案名稱']
                if inf_db[0].SpN != row['收單者']:
                    inf_db[0].SpN = row['收單者']
                if inf_db[0].CreWGro != row['申請部門']:
                    inf_db[0].CreWGro = row['申請部門']
                if inf_db[0].SR != row['需求分類']:
                    inf_db[0].SR = row['需求分類']
                if inf_db[0].CoxT != row['優先順序']:
                    inf_db[0].CoxT = row['優先順序']
                if inf_db[0].CreN != row['SR開單者']:
                    inf_db[0].CreN = row['SR開單者']
                if inf_db[0].Major != 0:
                    inf_db[0].Major = inf_db[0].Major
                if inf_db[0].State != "In Coming":
                    inf_db[0].State = inf_db[0].State
                db.session.commit()
            except IndexError:
                
                db.session.add(inf)
                db.session.commit()
        else:
            db.session.add(inf)
            db.session.commit()

if(sr_csv):
    df = pd.read_csv('order/SR.csv')
    df = df.fillna(value="")
    data_csv = df.to_dict(orient = 'records')
    for row in data_csv:
        inf = SR( row['Name'],
                  row['MVPN'],
                  row['Mail'])
        if (SR.query.filter_by(Name=str(row['Name'])).all() != None):
            inf_db = (SR.query.filter_by(Name=str(row['Name'])).all())
            try:
                if inf_db[0].Name != row['Name']:
                    inf_db[0].Name = row['Name']
                if row['MVPN'] != "":
                    if inf_db[0].MVPN != row['MVPN']:
                        inf_db[0].MVPN = row['MVPN']
                if inf_db[0].Mail != row['Mail']:
                    inf_db[0].Mail = row['Mail']
                sr_db.session.commit()
            except IndexError:
                sr_db.session.add(inf)
                sr_db.session.commit()
        else:
            sr_db.session.add(inf)
            sr_db.session.commit()
            
if(ad_csv):
    df = pd.read_csv('order/AD.csv')
    df = df.fillna(value="")
    data_csv = df.to_dict(orient = 'records')
    for row in data_csv:
        inf = AD( row['Name'],
                  row['Mail'],
                  row['PassWord'],
                  row['Permission'])
        if (AD.query.filter_by(Name=str(row['Name'])).all() != None):
            inf_db = (AD.query.filter_by(Name=str(row['Name'])).all())
            try:
                if inf_db[0].Name != row['Name']:
                    inf_db[0].Name = row['Name']
                if inf_db[0].Mail != row['Mail']:
                    inf_db[0].Mail = row['Mail']
                if inf_db[0].PassWord != row['PassWord']:
                    inf_db[0].PassWord = bcrypt.generate_password_hash(str(row['PassWord'])).decode('utf-8')
                if inf_db[0].Permission != row['Permission']:
                    inf_db[0].Permission = row['Permission']
                ad_db.session.commit()
            except IndexError:
                ad_db.session.add(inf)
                ad_db.session.commit()
        else:
            ad_db.session.add(inf)
            ad_db.session.commit()
qu = User.query.order_by("ID")

def get_page(offset=0, per_page=10, qu=qu):
    return qu[offset: offset + per_page]

@app.route('/',methods=['GET','POST'])
def index():
    quSR = SR.query.all()
    qu = User.query.filter_by(Major = "1").all()
    total = len(qu)  
    for i in range(total):
        qs = qu[i].StartDate.split("/")
        if(len(qs[1]) < 2):
           qs[1] = str(0)+qs[1]
        if(len(qs[2]) < 8):
           qs[2] = str(0)+qs[2]
        qu[i].StartDate = (qs[0]+"-"+qs[1]+"-"+qs[2]).replace(" ","T")
        qe = qu[i].EndDate.split("/")
        if(len(qe[1]) < 2):
           qe[1] = str(0)+qe[1]
        if(len(qe[2]) < 8):
           qe[2] = str(0)+qe[2]
        qu[i].EndDate = (qe[0]+"-"+qe[1]+"-"+qe[2]).replace(" ","T")
    
    sn = session.get('name')
    qu = User.query.all()
    total = len(qu)
    
    return render_template('calendar.html',qu=qu
                                          ,total=total
                                          ,arr=User.query.filter_by(Major = "1").all()
                                          ,quSR=quSR
                                          ,quAD=AD.query.filter_by(Name = sn).first()
                                          ,sn=sn)

@app.route('/fetnt', defaults={'page': 1})
@app.route('/fetnt/<page>')
@login_required
def fetnt(page):  
    qu = User.query.all()
    total = len(qu)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users = get_page(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            offset=offset,
                            total=total,
                            css_framework='bootstrap4')
    
    return render_template('FET_main.html',
                            qu=pagination_users,
                            pagination=pagination,
                            sad=AD.query.all())


@app.route('/search',methods=['GET','POST'])
def search():   
    qu = User.query.order_by("ID").all()
    if(request.method == 'POST'):
        if request.form.get('pos'):
            session['pos'] = False
            se = request.form.get('pos').strip()
            session['pos'] = se
            qu = User.query.filter(or_( User.ID.contains(session.get('pos')),
                                        User.StartDate.contains(session.get('pos')),
                                        User.EndDate.contains(session.get('pos')),
                                        User.Sub.contains(session.get('pos')),
                                        User.SpN.contains(session.get('pos')),
                                        User.CreWGro.contains(session.get('pos')),
                                        User.SR.contains(session.get('pos')),
                                        User.CoxT.contains(session.get('pos')),
                                        User.CreN.contains(session.get('pos')))).order_by("ID").all()
        if request.form.get('cancel'):
            session['pos'] = False
            qu = User.query.order_by("ID").all()
    elif session['pos'] == False:
        qu = User.query.order_by("ID").all()
    else:
        qu = User.query.filter(or_( User.ID.contains(session.get('pos')),
                                    User.StartDate.contains(session.get('pos')),
                                    User.EndDate.contains(session.get('pos')),
                                    User.Sub.contains(session.get('pos')),
                                    User.SpN.contains(session.get('pos')),
                                    User.CreWGro.contains(session.get('pos')),
                                    User.SR.contains(session.get('pos')),
                                    User.CoxT.contains(session.get('pos')),
                                    User.CreN.contains(session.get('pos')))).order_by("ID").all()
    total = len(qu)  
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users = get_page(offset=offset, per_page=per_page, qu=qu)
    
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            offset=offset,
                            total=total,
                            css_framework='bootstrap4')
    
    return render_template('FET_main.html',
                            qu=pagination_users,
                            pagination=pagination)

@app.route('/update',methods=['GET','POST'])
def update():
    if(path_csv):
        df = pd.read_csv('order/SR-Sample.csv', encoding='big5')
        df.replace("\r\n",'<br>', inplace=True,regex = True)
        df.replace("\n",'<br>', inplace=True,regex = True)
        df.replace("1(High)",'Critical', inplace=True)
        df.replace("2(Medium)",'Major', inplace=True)
        df.replace("3(Low)",'Minor', inplace=True)
        df = df.dropna()
        df = df.drop_duplicates(subset=["SR_ID"], keep="last")
        data_csv = df.to_dict(orient = 'records')
        for row in data_csv:
            row['Major'] = 0
            row['State'] = "In Coming"
            inf = User( row['SR_ID'],
                        row['PLAN_START_DATE_TEXT'],
                        row['PLAN_END_DATE_TEXT'],
                        row['SUBJECT'],
                        row['SPECIALIST_NAME'],
                        row['CREATOR_WORKGROUP_CODE'],
                        row['SR_SUB_CATEGORY'],
                        row['COX_TEXT'],
                        row['CREATOR_NAME'],
                        row['Major'],
                        row['State'])
            if (User.query.filter_by(ID=str(row['SR_ID'])).all() != None):
                inf_db = (User.query.filter_by(ID=str(row['SR_ID'])).all())
                try:
                    if inf_db[0].ID != row['SR_ID']:
                        inf_db[0].ID = row['SR_ID']
                    if inf_db[0].StartDate != row['PLAN_START_DATE_TEXT']:
                        inf_db[0].StartDate = row['PLAN_START_DATE_TEXT']
                    if inf_db[0].EndDate != row['PLAN_END_DATE_TEXT']:
                        inf_db[0].EndDate = row['PLAN_END_DATE_TEXT']
                    if inf_db[0].Sub != row['SUBJECT']:
                        inf_db[0].Sub = row['SUBJECT']
                    if inf_db[0].SpN != row['SPECIALIST_NAME']:
                        inf_db[0].SpN = row['SPECIALIST_NAME']
                    if inf_db[0].CreWGro != row['CREATOR_WORKGROUP_CODE']:
                        inf_db[0].CreWGro = row['CREATOR_WORKGROUP_CODE']
                    if inf_db[0].SR != row['SR_SUB_CATEGORY']:
                        inf_db[0].SR = row['SR_SUB_CATEGORY']
                    if inf_db[0].CoxT != row['COX_TEXT']:
                        inf_db[0].CoxT = row['COX_TEXT']
                    if inf_db[0].CreN != row['CREATOR_NAME']:
                        inf_db[0].CreN = row['CREATOR_NAME']
                    if inf_db[0].Major != 0:
                        inf_db[0].Major = inf_db[0].Major
                    if inf_db[0].State != "In Coming":
                        inf_db[0].State = inf_db[0].State
                    db.session.commit()
                except IndexError:
                    db.session.add(inf)
                    db.session.commit()
            else:
                db.session.add(inf)
                db.session.commit()
                
    if(path_excel):
        df = pandas.read_excel("order/SRTT.xls", usecols=['SR編號', '開始日期', '結束日期', '測試專案名稱', '收單者', '申請部門', '需求分類', '優先順序', 'SR開單者'])
        df.replace("",'', inplace=True,regex = True)
        df = df.dropna()
        data_excel = df.to_dict(orient = 'records')
        for row in data_excel:
            row['Major'] = 0
            row['State'] = "In Coming"
            inf = User( row['SR編號'],
                        row['開始日期'],
                        row['結束日期'],
                        row['測試專案名稱'],
                        row['收單者'],
                        row['申請部門'],
                        row['需求分類'],
                        row['優先順序'],
                        row['SR開單者'],
                        row['Major'],
                        row['State'])
            if (User.query.filter_by(ID=str(row['SR編號'])).all() != None):
                inf_db = (User.query.filter_by(ID=str(row['SR編號'])).all())
                try:
                    if inf_db[0].ID != row['SR編號']:
                        inf_db[0].ID = row['SR編號']
                    if inf_db[0].StartDate != row['開始日期']:
                        inf_db[0].StartDate = row['開始日期']
                    if inf_db[0].EndDate != row['結束日期']:
                        inf_db[0].EndDate = row['結束日期']
                    if inf_db[0].Sub != row['測試專案名稱']:
                        inf_db[0].Sub = row['測試專案名稱']
                    if inf_db[0].SpN != row['收單者']:
                        inf_db[0].SpN = row['收單者']
                    if inf_db[0].CreWGro != row['申請部門']:
                        inf_db[0].CreWGro = row['申請部門']
                    if inf_db[0].SR != row['需求分類']:
                        inf_db[0].SR = row['需求分類']
                    if inf_db[0].CoxT != row['優先順序']:
                        inf_db[0].CoxT = row['優先順序']
                    if inf_db[0].CreN != row['SR開單者']:
                        inf_db[0].CreN = row['SR開單者']
                    if inf_db[0].Major != 0:
                        inf_db[0].Major = inf_db[0].Major
                    if inf_db[0].State != "In Coming":
                        inf_db[0].State = inf_db[0].State
                    db.session.commit()
                except IndexError:
                    db.session.add(inf)
                    db.session.commit()
            else:
                db.session.add(inf)
                db.session.commit()
            
    qu = User.query.order_by("ID")
    
    def get_page(offset=0, per_page=10, qu=qu):
        return qu[offset: offset + per_page]

    qu = User.query.all()
    total = len(qu)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users = get_page(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            offset=offset,
                            total=total,
                            css_framework='bootstrap4')
    
    return render_template('FET_main.html',
                            qu=pagination_users,
                            pagination=pagination)

@app.route('/revise/<ID>',methods=['GET','POST'])
def revise(ID):
    if(request.method == 'POST'):
        rev = request.form.get("sub")
        sel = request.form.get("sel")
        
        Users = User.query.filter_by(ID=str(ID)).first()
        Users.Sub = str(rev)
        Users.State = str(sel)
        if(request.form.get("cb") == None):
            Users.Major = 0  
        else:
            Users.Major = 1  
        
        db.session.commit()
        
        qu = User.query.order_by("ID")
        total = len(User.query.all())  
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        pagination_users = get_page(offset=offset, per_page=per_page, qu=qu)
        pagination = Pagination(page=page, 
                                per_page=per_page, 
                                offset=offset,
                                total=total,
                                css_framework='bootstrap4')
        
        return render_template('FET_main.html',
                                qu=pagination_users,
                                pagination=pagination)


@app.route('/calendar_ne',methods=['GET','POST'])
def calendar_ne():
    if(request.method == 'POST'):
        sName = request.form.get("Name")
        sMVPN = request.form.get("MVPN")
        sMail = request.form.get("Mail")
        if(sName != "" and sMail != ""):
            if(SR.query.filter_by(Name = sName).first() == None) and (SR.query.filter_by(Mail = sMail).first() == None):
                NPe = SR(sName, sMVPN, sMail)
                sr_db.session.add(NPe)
                sr_db.session.commit()
            
    sn = session.get('name')
    quSR = SR.query.all()
    qu = User.query.filter_by(Major = "1").all()
    total = len(qu)  
    for i in range(total):
        qs = qu[i].StartDate.split("/")
        if(len(qs[1]) < 2):
           qs[1] = str(0)+qs[1]
        if(len(qs[2]) < 8):
           qs[2] = str(0)+qs[2]
        qu[i].StartDate = (qs[0]+"-"+qs[1]+"-"+qs[2]).replace(" ","T")
        qe = qu[i].EndDate.split("/")
        if(len(qe[1]) < 2):
           qe[1] = str(0)+qe[1]
        if(len(qe[2]) < 8):
           qe[2] = str(0)+qe[2]
        qu[i].EndDate = (qe[0]+"-"+qe[1]+"-"+qe[2]).replace(" ","T")
            
    return render_template('calendar.html',qu=qu
                                          ,total=total
                                          ,arr=User.query.filter_by(Major = "1").all()
                                          ,quSR=quSR
                                          ,quAD=AD.query.all()
                                          ,sn=sn)

@app.route('/calendar_ch/<ID>',methods=['GET','POST'])
def calendar_ch(ID):
    if(request.method == 'POST'):
        SName = request.form.get("CName")
        SMVPN = request.form.get("CMVPN")
        SMail = request.form.get("CMail")
        nSR = SR.query.filter_by(Name=str(ID)).first()
        if(SR.query.filter_by(Name = SName).first() == None) or (SR.query.filter_by(Name = SName).first() == SName):
            nSR.Name = str(SName)  
            sr_db.session.commit()
        if (SR.query.filter_by(Mail = SMail).first() == None) or (SR.query.filter_by(Mail = SMail).first() == SMail):
            nSR.Mail = str(SMail)
            sr_db.session.commit()
        if(SR.query.filter_by(MVPN = SMVPN).first() == None) or (SR.query.filter_by(MVPN = SMVPN).first() == SMail):
            nSR.MVPN = str(SMVPN)
            sr_db.session.commit()
        if(SName == ""):
            sr_db.session.delete(nSR)            
            sr_db.session.commit()
        
    sn = session.get('name')
    quSR = SR.query.all()
    qu = User.query.filter_by(Major = "1").all()
    total = len(qu)  
    for i in range(total):
        qs = qu[i].StartDate.split("/")
        if(len(qs[1]) < 2):
           qs[1] = str(0)+qs[1]
        if(len(qs[2]) < 8):
           qs[2] = str(0)+qs[2]
        qu[i].StartDate = (qs[0]+"-"+qs[1]+"-"+qs[2]).replace(" ","T")
        qe = qu[i].EndDate.split("/")
        if(len(qe[1]) < 2):
           qe[1] = str(0)+qe[1]
        if(len(qe[2]) < 8):
           qe[2] = str(0)+qe[2]
        qu[i].EndDate = (qe[0]+"-"+qe[1]+"-"+qe[2]).replace(" ","T")
            
    return render_template('calendar.html',qu=qu
                                          ,total=total
                                          ,arr=User.query.filter_by(Major = "1").all()
                                          ,quSR=quSR
                                          ,quAD=AD.query.all()
                                          ,sn=sn)

@app.route('/Mojor',methods=['GET','POST'])
def Mojor():
    qu = User.query.filter_by(Major = "1").all()
    total = len(qu)  
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users = get_page(offset=offset, per_page=per_page, qu=qu)
    
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            offset=offset,
                            total=total,
                            css_framework='bootstrap4')
    
    return render_template('FET_main.html',
                            qu=pagination_users,
                            pagination=pagination)

@app.route('/mailTest/<ID>',methods=['GET','POST'])
def mailTest(ID):
    if(request.method == 'POST'):
        Users = User.query.filter_by(ID=str(ID)).first()
        smsg = request.form.get("msg")
        sents = request.form.getlist("SMail")
        recipient = ""
        for i in range(len(sents)):
            recipient += sents[i]+","
        ma = "1. SR#" + Users.ID + "：" + Users.Sub + "\r\n" + "2. " 
        SpN = "實驗室支援: " + Users.SpN + "\r\n" 
        msg = "3. " + smsg
        content = MIMEMultipart() 
        content["subject"] = "Major SR 狀態更新"
        content["from"] = "smartfetelab@gmail.com"
        content["to"] = recipient
        SpN = "實驗室支援: " + Users.SpN + "\r\n" 
        content.attach(MIMEText(ma+SpN+msg))
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
            try:
                smtp.ehlo()
                smtp.starttls()
                smtp.login("smartfetelab@gmail.com", "klingpbxmgptihmm")
                smtp.send_message(content)
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)
        
    
    sn = session.get('name')
    quSR = SR.query.all()
    qu = User.query.filter_by(Major = "1").all()
    total = len(qu)  
    for i in range(total):
        qs = qu[i].StartDate.split("/")
        if(len(qs[1]) < 2):
           qs[1] = str(0)+qs[1]
        if(len(qs[2]) < 8):
           qs[2] = str(0)+qs[2]
        qu[i].StartDate = (qs[0]+"-"+qs[1]+"-"+qs[2]).replace(" ","T")
        qe = qu[i].EndDate.split("/")
        if(len(qe[1]) < 2):
           qe[1] = str(0)+qe[1]
        if(len(qe[2]) < 8):
           qe[2] = str(0)+qe[2]
        qu[i].EndDate = (qe[0]+"-"+qe[1]+"-"+qe[2]).replace(" ","T")
            
    return render_template('calendar.html',qu=qu
                                          ,total=total
                                          ,arr=User.query.filter_by(Major = "1").all()
                                          ,quSR=quSR
                                          ,quAD=AD.query.all()
                                          ,sn=sn)

@app.route('/mailEnd/<ID>',methods=['GET','POST'])
def mailEnd(ID):
    if(request.method == 'POST'):
        Users = User.query.filter_by(ID=str(ID)).first()
        date = request.form.get("date")
        tot = request.form.get("tot")
        mpass = request.form.get("mpass")
        fail = request.form.get("fail")
        no = request.form.get("no")
        sents = request.form.get("SMail")
        content = MIMEMultipart() 
        content["subject"] = "Major SR 狀態更新" 
        content["from"] = "smartfetelab@gmail.com" 
        content["to"] = sents
        ma = "1. SR#" + Users.ID + "：" + Users.Sub + "\r\n" 
        SpN = "2. 實驗室支援: " + Users.SpN + "\r\n" 
        msg = "3. 已於 " + date + " 結束測試 " + "\r\n" 
        msg += "4. 共 " + tot + " 測試 " + "\r\n" 
        msg += "    Pass: " + mpass + " 項 " + "\r\n" 
        msg += "    Fail: " + fail + " 項 " + "\r\n" 
        msg += "    無環境測試: " + no + " 項 " 
        content.attach(MIMEText(ma+SpN+msg))
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
            try:
                smtp.ehlo() 
                smtp.starttls() 
                smtp.login("smartfetelab@gmail.com", "klingpbxmgptihmm")
                smtp.send_message(content)
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)
        
    
    sn = session.get('name')
    quSR = SR.query.all()
    qu = User.query.filter_by(Major = "1").all()
    total = len(qu)  
    for i in range(total):
        qs = qu[i].StartDate.split("/")
        if(len(qs[1]) < 2):
           qs[1] = str(0)+qs[1]
        if(len(qs[2]) < 8):
           qs[2] = str(0)+qs[2]
        qu[i].StartDate = (qs[0]+"-"+qs[1]+"-"+qs[2]).replace(" ","T")
        qe = qu[i].EndDate.split("/")
        if(len(qe[1]) < 2):
           qe[1] = str(0)+qe[1]
        if(len(qe[2]) < 8):
           qe[2] = str(0)+qe[2]
        qu[i].EndDate = (qe[0]+"-"+qe[1]+"-"+qe[2]).replace(" ","T")
            
    return render_template('calendar.html',qu=qu
                                          ,total=total
                                          ,arr=User.query.filter_by(Major = "1").all()
                                          ,quSR=quSR
                                          ,quAD=AD.query.all()
                                          ,sn=sn)


class adUser(UserMixin):
    pass

@login_manager.user_loader
def user_loader(SUser):
    if SUser not in users:
        return

    auser = adUser()
    auser.id = SUser  
    return auser

@login_manager.request_loader
def request_loader(request):
    SUser = request.form.get("PMail")
    if SUser not in users:
        return

    auser = adUser()
    auser.id = SUser  
    return auser

adSR = AD.query.all()
if AD.query.count() == 0:
    users = {"": {'password': ""}}
else:
    users = {adSR[0].Mail: {'password': adSR[0].PassWord}}

for i in range(AD.query.count()):
    if i == 0:
        continue
    ensm = adSR[i].Mail
    ensp = adSR[i].PassWord
    users.update({ensm: {'password': ensp}})

@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        PMail = request.form.get("PMail")
        Ppass = request.form.get("Ppass")
        session['id'] = PMail
        session['name'] = ""
        
        adSR = AD.query.all()
        if AD.query.count() == 0:
            users = {"": {'password': ""}}
        else:
            users = {adSR[0].Mail: {'password': adSR[0].PassWord}}
        
        for i in range(AD.query.count()):
            if i == 0:
                continue
            ensm = adSR[i].Mail
            ensp = adSR[i].PassWord
            users.update({ensm: {'password': ensp}})
        try:
            if AD.query.filter_by(Mail = str(PMail)).first() != None:
                if bcrypt.check_password_hash(str(users[PMail]['password']), Ppass) == True:
                    qad = AD.query.filter_by(Mail = str(PMail)).first()
                    session['name'] = qad.Name
                    auser = adUser()
                    auser.id = session.get('id')
                    login_user(auser)
            else:
                pass
        except TypeError:
            pass                  
        except KeyError:
            pass    
    sn = session.get('name')
    quSR = SR.query.all()
    qu = User.query.filter_by(Major = "1").all()
    total = len(qu)  
    for i in range(total):
        qs = qu[i].StartDate.split("/")
        if(len(qs[1]) < 2):
           qs[1] = str(0)+qs[1]
        if(len(qs[2]) < 8):
           qs[2] = str(0)+qs[2]
        qu[i].StartDate = (qs[0]+"-"+qs[1]+"-"+qs[2]).replace(" ","T")
        qe = qu[i].EndDate.split("/")
        if(len(qe[1]) < 2):
           qe[1] = str(0)+qe[1]
        if(len(qe[2]) < 8):
           qe[2] = str(0)+qe[2]
        qu[i].EndDate = (qe[0]+"-"+qe[1]+"-"+qe[2]).replace(" ","T")
    
    
    return render_template('calendar.html',qu=qu
                                          ,total=total
                                          ,arr=User.query.filter_by(Major = "1").all()
                                          ,quSR=quSR
                                          ,quAD=AD.query.filter_by(Name = sn).first()
                                          ,sn=sn)

@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    quSR = SR.query.all()
    qu = User.query.filter_by(Major = "1").all()
    total = len(qu)  
    for i in range(total):
        qs = qu[i].StartDate.split("/")
        if(len(qs[1]) < 2):
           qs[1] = str(0)+qs[1]
        if(len(qs[2]) < 8):
           qs[2] = str(0)+qs[2]
        qu[i].StartDate = (qs[0]+"-"+qs[1]+"-"+qs[2]).replace(" ","T")
        qe = qu[i].EndDate.split("/")
        if(len(qe[1]) < 2):
           qe[1] = str(0)+qe[1]
        if(len(qe[2]) < 8):
           qe[2] = str(0)+qe[2]
        qu[i].EndDate = (qe[0]+"-"+qe[1]+"-"+qe[2]).replace(" ","T")
    
    
    return render_template('calendar.html',qu=qu
                                          ,total=total
                                          ,arr=User.query.filter_by(Major = "1").all()
                                          ,quSR=quSR
                                          ,quAD=AD.query.all())

@app.route('/register', methods=['GET','POST'])
def register():
    if(request.method == 'POST'):
        Ruser = request.form.get("Rname")
        Rmail = request.form.get("Rmail")
        Rpassword = request.form.get("Rpass")
        if(AD.query.filter_by(Name = str(Ruser)).first() == None):
            p_hash = bcrypt.generate_password_hash(Rpassword).decode('utf-8')
            RUser = AD(Ruser, Rmail, p_hash, "0")
            ad_db.session.add(RUser)
            ad_db.session.commit()
        
    qu = User.query.all()
    total = len(qu)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users = get_page(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            offset=offset,
                            total=total,
                            css_framework='bootstrap4')
    
    return render_template('FET_main.html',
                            qu=pagination_users,
                            pagination=pagination)
@app.route('/addnt', methods=['GET','POST'])
def addnt():  
    if(request.method == 'POST'):
        srid = request.form.get("srid")
        srsu = request.form.get("srsu")
        srbi = request.form.get("srbi")
        srla = request.form.get("srla")
        srsta = request.form.get("srsta")
        sren = request.form.get("sren")
        srst = request.form.get("srst")
        srde = request.form.get("srde")
        srca = request.form.get("srca")
        srma = request.form.get("srma")
        
        st = srsta.split("-")
        sta = st[2].split("T")
        srsta = st[0]+"/"+st[1]+"/"+sta[0]+" "+sta[1]
        
        sen = sren.split("-")
        send = sen[2].split("T")
        sren = sen[0]+"/"+sen[1]+"/"+send[0]+" "+send[1]
        
        if(User.query.filter_by(ID = str(srid)).first() == None):
            addnt = User(srid, srsta, sren, srsu, srla, srde, srca, srma, srbi, "0", srst)
            db.session.add(addnt)
            db.session.commit()
    qu = User.query.all()
    total = len(qu)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users = get_page(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            offset=offset,
                            total=total,
                            css_framework='bootstrap4')
    
    return render_template('FET_main.html',
                            qu=pagination_users,
                            pagination=pagination)      
today = date.today()
qus = User.query.filter_by(Major = "1").all()
total = len(qus)  
for i in range(total):
    sd = qus[i].StartDate
    qs = qus[i].StartDate.split("/")
    qss = qs[2].split(" ")
    if(len(qs[1]) < 2):
        qs[1] = str(0)+qs[1]
    if(len(qss[0]) < 2):
        qss[0] = str(0)+qss[0]
    if(str(today) == str(qs[0]+"-"+qs[1]+"-"+qss[0])):
        @scheduler.task('interval', id='job', start_date=str(today)+" 06:00:00",end_date=str(today)+" 06:00:00")
        def job():
            Users = User.query.filter_by(StartDate = str(sd)).first()
            sent = "cdchang@fareastone.com.tw,vchiang@fareastone.com.tw,sheyang@fareastone.com.tw,tcyang@fareastone.com.tw"
            se1 = AD.query.filter_by(Name = str(Users.SpN)).first()
            se2 = AD.query.filter_by(Name = str(Users.CreN)).first()
            if(se1 != None):
                sent = sent + "," + se1.Mail
            if(se2 != None):
                sent = sent + "," + se2.Mail
            content = MIMEMultipart()
            content["subject"] = "Major SR 狀態更新"
            content["from"] = "smartfetelab@gmail.com"
            content["to"] = sent  
            ma = "1. " + "SR#" + str(Users.ID) + "：" + str(Users.Sub) + "\r\n" 
            SpN = "2. 實驗室支援: " + str(Users.SpN) + "\r\n" 
            StD = "3. 於今日" + str(sd) + "開始測試" + "\r\n"
            EnD = "4. 預計" + str(Users.EndDate) + "結束測試" 
            content.attach(MIMEText(ma+SpN+StD+EnD))
            with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
                try:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login("smartfetelab@gmail.com", "klingpbxmgptihmm")
                    smtp.send_message(content) 
                except Exception as e:
                    print("Error message: ", e)
    
if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    # app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    app.run(host="0.0.0.0", port=8080, debug=True)

