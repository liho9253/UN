from FET_user import User
from FET_user import db
from SR_db import SR
from SR_db import sr_db
from SR_ad import AD
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

app = Flask(__name__)

scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.urandom(24)

path_csv = os.path.isfile('order/SR-Sample.csv')
path_excel = os.path.isfile('order/SRTT.xls')
 
db.init_app(app)
sr_db.init_app(app)

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
    df = pandas.read_excel("order/SRTT.xls")
    df.replace("",'', inplace=True,regex = True)
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

@app.route('/', defaults={'page': 1})
@app.route('/<page>')
def index(page):
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
        df = pandas.read_excel("order/SRTT.xls")
        df.replace("",'', inplace=True,regex = True)
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
        sd = request.form.get("sd")
        ed = request.form.get("ed")
        sel = request.form.get("sel")
        
        Users = User.query.filter_by(ID=str(ID)).first()
        Users.Sub = str(rev)
        Users.StartDate = str(sd)  
        Users.EndDate = str(ed)
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

@app.route('/calendar',methods=['GET','POST'])
def calendar():
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

@app.route('/calendar_ch/<ID>',methods=['GET','POST'])
def calendar_ch(ID):
    if(request.method == 'POST'):
        SName = request.form.get("SName")
        SMVPN = request.form.get("SMVPN")
        SMail = request.form.get("SMail")
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

@app.route('/mailSt/<ID>',methods=['GET','POST'])
def mailSt(ID):
    Users = User.query.filter_by(ID=str(ID)).first()
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "Major SR 狀態更新" #郵件標題
    content["from"] = "smartfetelab@gmail.com"  #寄件者
    content["to"] = "timmy89566@gmail.com" #收件者
    ma = "1. " + "SR#" + Users.ID + "：" + Users.Sub + "\r\n" 
    SpN = "2. 實驗室支援: " + Users.SpN + "\r\n" 
    StD = "3. 於今日" + Users.StartDate + "開始測試" + "\r\n"
    EnD = "4. 預計" + Users.EndDate + "結束測試" 
    content.attach(MIMEText(ma+SpN+StD+EnD))
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("smartfetelab@gmail.com", "klingpbxmgptihmm")
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)
            
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
        content = MIMEMultipart()  #建立MIMEMultipart物件
        content["subject"] = "Major SR 狀態更新"  #郵件標題
        content["from"] = "smartfetelab@gmail.com"  #寄件者
        content["to"] = recipient #收件者
        SpN = "實驗室支援: " + Users.SpN + "\r\n" 
        content.attach(MIMEText(ma+SpN+msg))
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("smartfetelab@gmail.com", "klingpbxmgptihmm")
                smtp.send_message(content)  # 寄送郵件
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)
        
    
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
        content = MIMEMultipart()  #建立MIMEMultipart物件
        content["subject"] = "Major SR 狀態更新"  #郵件標題
        content["from"] = "smartfetelab@gmail.com"  #寄件者
        content["to"] = sents #收件者
        ma = "1. SR#" + Users.ID + "：" + Users.Sub + "\r\n" 
        SpN = "2. 實驗室支援: " + Users.SpN + "\r\n" 
        msg = "3. 已於 " + date + " 結束測試 " + "\r\n" 
        msg += "4. 共 " + tot + " 測試 " + "\r\n" 
        msg += "    Pass: " + mpass + " 項 " + "\r\n" 
        msg += "    Fail: " + fail + " 項 " + "\r\n" 
        msg += "    無環境測試: " + no + " 項 " 
        content.attach(MIMEText(ma+SpN+msg))
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("smartfetelab@gmail.com", "klingpbxmgptihmm")
                smtp.send_message(content)  # 寄送郵件
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)
        
    
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
            content = MIMEMultipart()  #建立MIMEMultipart物件
            content["subject"] = "Major SR 狀態更新" #郵件標題
            content["from"] = "timmy89566@gmail.com"  #寄件者
            content["to"] = "timmy89566@gmail.com" #收件者
            ma = "1. " + "SR#" + str(Users.ID) + "：" + str(Users.Sub) + "\r\n" 
            SpN = "2. 實驗室支援: " + str(Users.SpN) + "\r\n" 
            StD = "3. 於今日" + str(sd) + "開始測試" + "\r\n"
            EnD = "4. 預計" + str(Users.EndDate) + "結束測試" 
            content.attach(MIMEText(ma+SpN+StD+EnD))
            with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
                try:
                    smtp.ehlo()  # 驗證SMTP伺服器
                    smtp.starttls()  # 建立加密傳輸
                    smtp.login("timmy89566@gmail.com", "nsajrwcqpwuqrcld")
                    smtp.send_message(content)  # 寄送郵件
                    # print(str(qus[i].StartDate))
                except Exception as e:
                    print("Error message: ", e)
    
    
if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

