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
    inf = User( row['SR_ID'],
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
    inf_list = [row['SR_ID'],
                row['PLAN_START_DATE_TEXT'],
                row['PLAN_END_DATE_TEXT'],
                row['SUBJECT'],
                row['SPECIALIST_NAME'],
                row['CLOSE_DATE_TEXT'],
                row['CREATOR_WORKGROUP_CODE'],
                row['SR_SUB_CATEGORY'],
                row['COX_TEXT'],
                row['DESCRIPTION'],
                row['CREATOR_NAME']]
    if (User.query.filter_by(ID=str(row['SR_ID'])).all() != None):
        inf_db = (User.query.filter_by(ID=str(row['SR_ID'])).all())
        infdb_list = []
        try:
            infdb_list.append(inf_db[0].ID)
            infdb_list.append(inf_db[0].StartDate)
            infdb_list.append(inf_db[0].EndDate)
            infdb_list.append(inf_db[0].Sub)
            infdb_list.append(inf_db[0].SpN)
            infdb_list.append(inf_db[0].CloseDate)
            infdb_list.append(inf_db[0].CreWGro)
            infdb_list.append(inf_db[0].SR)
            infdb_list.append(inf_db[0].CoxT)
            infdb_list.append(inf_db[0].Dec)
            infdb_list.append(inf_db[0].CreN)
            if(inf_list == infdb_list):
                continue
            else:
                User.query.filter_by(ID=str(row['SR_ID'])).delete()
                db.session.commit()
                db.session.add(inf)
                db.session.commit()
        except IndexError:
            db.session.add(inf)
            db.session.commit()
    else:
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
                                        User.SR.contains(session.get('pos')),
                                        User.CoxT.contains(session.get('pos')),
                                        User.Dec.contains(session.get('pos')),
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
@app.route('/delete/<ID>')
def delete(ID):
    User.query.filter_by(ID=str(ID)).delete()
    db.session.commit()
    
    qu = User.query.all()
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
@app.route('/revise/<ID>',methods=['GET','POST'])
def revise(ID):
    rev = request.form.get("sub")
    Users = User.query.filter_by(ID=str(ID)).first()
    Users.Sub = str(rev)
    db.session.commit()
    
    qu = User.query.all()
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
if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=True)

