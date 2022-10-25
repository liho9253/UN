from acupDB import Acup
from acupDB import adb
from flask import Flask, render_template, request, session
import pandas as pd
import pandas, os
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.urandom(24)

adb.init_app(app)

path_txt = os.path.isfile('acupall.csv')
if(path_txt):
    df = pd.read_csv('acupall.csv', error_bad_lines=False)
    df = df.drop_duplicates(subset=["acup_id"], keep="last")
    df = df.fillna("")
    data_txt = df.to_dict(orient = 'records')
    for row in data_txt:
        inf = Acup( row['merd_id'],
                    row['acup_id'],
                    row['acup_name'],
                    row['acup_alias'],
                    row['acup_take'],
                    row['acpu_acupuncture'],
                    row['acpu_function'],
                    row['acpu_indications'])
        if (Acup.query.filter_by(acup_id=str(row['acup_id'])).all() != None):
            inf_db = (Acup.query.filter_by(acup_id=str(row['acup_id'])).all())
            try:
                if inf_db[0].merd_id != row['merd_id']:
                    inf_db[0].merd_id = row['merd_id']
                if inf_db[0].acup_id != row['acup_id']:
                    inf_db[0].acup_id = row['acup_id']
                if inf_db[0].acup_name != row['acup_name']:
                    inf_db[0].acup_name = row['acup_name']
                if inf_db[0].acup_alias != row['acup_alias']:
                    inf_db[0].acup_alias = row['acup_alias']
                if inf_db[0].acup_take != row['acup_take']:
                    inf_db[0].acup_take = row['acup_take']
                if inf_db[0].acpu_acupuncture != row['acpu_acupuncture']:
                    inf_db[0].acpu_acupuncture = row['acpu_acupuncture']
                if inf_db[0].acpu_function != row['acpu_function']:
                    inf_db[0].acpu_function = row['acpu_function']
                if inf_db[0].acpu_indications != row['acpu_indications']:
                    inf_db[0].acpu_indications = row['acpu_indications']
                adb.session.commit()
            except IndexError:
                adb.session.add(inf)
                adb.session.commit()
        else:
            adb.session.add(inf)
            adb.session.commit()


@app.route('/',methods=['GET','POST'])
def index():
    return 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)















