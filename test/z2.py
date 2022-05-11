from FET_user import User
from FET_user import db
from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import or_
import pandas

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

df = pandas.read_csv('test16.csv')
df.replace("\r\n",'<br>', inplace=True,regex = True)
data = df.to_dict(orient = 'records')

for row in data:
    if (row['SR_ID'] != ""):
        continue
            
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
    db.session.add(inf)
    db.session.commit()

qu = User.query.all()

def get_page(offset=0, per_page=10, qu=qu):
    return qu[offset: offset + per_page]
@app.route('/')

def index():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users = get_page(offset=offset, per_page=per_page)
    
    # 頁數
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
    se = request.form['username'].strip()
    qu = User.query.filter_by(ID=se).all()
    
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users = get_page(offset=offset, per_page=per_page, qu=qu)
    
    total = len(qu)
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            css_framework='bootstrap4')
    
    return render_template('FET_main.html',
                            qu=pagination_users,
                            pagination=pagination)

if __name__ == "__main__":
    
    app.run(host="localhost", port=5000, debug=True)

