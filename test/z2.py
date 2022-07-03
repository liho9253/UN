from FET_user import User
from FET_user import db
from flask import Flask, render_template, request, session
from flask_paginate import Pagination, get_page_args
from sqlalchemy import or_
import pandas as pd
import pandas, os
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)

df = pandas.read_csv('test16.csv')
df.replace("\r\n",'<br>', inplace=True,regex = True)
df.replace("\n",'<br>', inplace=True,regex = True)
data = df.to_dict(orient = 'records')
df = df.dropna()
df = df.drop_duplicates(subset=["SR_ID"], keep="last")
df.to_csv("test16.csv",encoding = 'utf-8',index=False)
df = pd.read_csv('./test16.csv',encoding = 'utf-8')

for row in data:
    row['Major'] = 0
    row['State'] = "In Coming"
    inf = User( row['SR_ID'],
                row['PLAN_START_DATE_TEXT'],
                row['PLAN_END_DATE_TEXT'],
                row['SUBJECT'],
                row['SPECIALIST_NAME'],
                row['CLOSE_DATE_TEXT'],
                row['CREATOR_WORKGROUP_CODE'],
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
            if inf_db[0].CloseDate != row['CLOSE_DATE_TEXT']:
                inf_db[0].CloseDate = row['CLOSE_DATE_TEXT']
            if inf_db[0].CreWGro != row['CREATOR_WORKGROUP_CODE']:
                inf_db[0].CreWGro = row['CREATOR_WORKGROUP_CODE']
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
        
qu = User.query.order_by("ID")

def get_page(offset=0, per_page=10, qu=qu):
    return qu[offset: offset + per_page]

@app.route('/')
def index():
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
    qu = User.query.all()
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
                                        User.CloseDate.contains(session.get('pos')),
                                        User.CreWGro.contains(session.get('pos')),
                                        User.CoxT.contains(session.get('pos')),
                                        User.CreN.contains(session.get('pos')))).all()
        if request.form.get('cancel'):
            session['pos'] = False
            qu = User.query.all()
    elif session['pos'] == False:
        qu = User.query.all()
    else:
        qu = User.query.filter(or_( User.ID.contains(session.get('pos')),
                                    User.StartDate.contains(session.get('pos')),
                                    User.EndDate.contains(session.get('pos')),
                                    User.Sub.contains(session.get('pos')),
                                    User.SpN.contains(session.get('pos')),
                                    User.CloseDate.contains(session.get('pos')),
                                    User.CreWGro.contains(session.get('pos')),
                                    User.SR.contains(session.get('pos')),
                                    User.CoxT.contains(session.get('pos')),
                                    User.Dec.contains(session.get('pos')),
                                    User.CreN.contains(session.get('pos')))).all()
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

@app.route('/update',methods=['GET','POST'])
def update():
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

@app.route('/ChangeTime',methods=['GET','POST'])
def ChangeTime(ID):
    input("時:")
    input("分:")
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

    return render_template('calendar.html')
if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=True)

