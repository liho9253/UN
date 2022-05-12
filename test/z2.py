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
    if (User.query.filter_by(ID=str(row['SR_ID'])).all() != ""):
        qu = User.query.filter(or_(User.StartDate == row['PLAN_START_DATE_TEXT'],
                                   User.EndDate == row['PLAN_END_DATE_TEXT'],
                                   User.Sub == row['SUBJECT'],
                                   User.SpN == row['SPECIALIST_NAME'],
                                   User.CloseDate == row['CLOSE_DATE_TEXT'],
                                   User.CreWGro == row['CREATOR_WORKGROUP_CODE'],
                                   User.SR == row['SR_SUB_CATEGORY'],
                                   User.CoxT == row['COX_TEXT'],
                                   User.Dec == row['DESCRIPTION'],
                                   User.CreN == row['CREATOR_NAME'])).all()
        continue
    else:
        de = User.query.filter_by(ID=str(row['SR_ID'])).all()
        inf = User(row['SR_ID'],
                   row['PLAN_START_DATE_TEXT'],
                   row['PLAN_END_DATE_TEXT'],
                   row['SUBJECT'],
                   row['SPECIALIST_NAME'],
                   row['CLOSE_DATE_TEXT'],
                   row['CREATOR_WORKGROUP_CODE'],
                   row['SR_SUB_CATEGORY'],
                   row['COX_TEXT'],
                   row['DESCRIPTION'],
                   row['CREATOR_NAME'])
        db.session.delete(de)
        db.session.commit()
        db.session.add(inf)
        db.session.commit()
        
qu = User.query.all()

def get_page(offset=0, per_page=10, qu=qu):
    return qu[offset: offset + per_page]

@app.route('/')
def index():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users = get_page(offset=offset, per_page=per_page)
    
    total = len(qu)
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            css_framework='bootstrap4')
    
    return render_template('FET_main.html',
                            qu=pagination_users,
                            pagination=pagination)


@app.route('/search',methods=['GET','POST'])
def search():
    session['pos'] = False
    if(request.form['pos'] != ''):
        se = request.form['pos'].strip()
        session['pos'] = se
    
        qu = User.query.filter(or_( User.ID.contains(session.get('pos')),
                                    User.StartDate.contains(se),
                                    User.EndDate.contains(se),
                                    User.Sub.contains(se),
                                    User.SpN.contains(se),
                                    User.CloseDate.contains(se),
                                    User.CreWGro.contains(se),
                                    User.SR.contains(se),
                                    User.CoxT.contains(se),
                                    User.Dec.contains(se),
                                    User.CreN.contains(se))).all()
    else:
        qu = User.query.all() 
                         
    total = len(qu)  
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users = get_page(offset=offset, per_page=per_page, qu=qu)
    
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            css_framework='bootstrap4')
    
    return render_template('FET_main.html',
                            qu=pagination_users,
                            pagination=pagination)

if __name__ == "__main__":
    
    app.run(host="localhost", port=5000, debug=True)

