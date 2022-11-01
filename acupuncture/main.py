from acupDB import Acup
from acupDB import adb
from merDB import Mer
from merDB import mad
from flask import Flask, render_template, request, session
from flask_paginate import Pagination, get_page_args
import pandas as pd
import pandas, os
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

db = SQLAlchemy()
app = Flask(__name__)
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.urandom(24)

adb.init_app(app)
mad.init_app(app)

path_txt = os.path.isfile('acupalls.csv')
if(path_txt):
    df = pd.read_csv('acupall.csv', error_bad_lines=False)
    df = df.drop_duplicates(subset=["acup_id"], keep="last")
    df = df.fillna("")
    data_txt = df.to_dict(orient = 'records')
    for row in data_txt:
        inf = Acup( row['merd_id'],
                    row['acup_id'],
                    row['acup_name'],
                    row['acup_enname'],
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
                if inf_db[0].acup_enname != row['acup_enname']:
                    inf_db[0].acup_enname = row['acup_enname']
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
    
    
    
    
    return render_template('BL01.html')


@app.route('/encyclopedia',methods=['GET','POST'])
def encyclopedia():
    qu = Mer.query.order_by("merd_name").all()
    sn = "十二經脈與經外奇穴"
    return render_template('encyclopedia.html',
                           qu=qu,
                           sn=sn)

@app.route('/model',methods=['GET','POST'])
def model():
    
    return render_template('model.html')

@app.route('/monitor',methods=['GET','POST'])
def monitor():
    
    return render_template('monitor.html')


@app.route('/search',methods=['GET','POST'])
def search():   
    qu = Mer.query.order_by("merd_name").all()
    session['pos'] = False
    if(request.method == 'POST'):
        if request.form.get('pos'):
            if request.form.get('cho') == "aname":
                se = request.form.get('pos').strip()
                session['pos'] = se
                qu = Acup.query.filter(Acup.acup_name.contains(session.get('pos'))).order_by("acup_name").all()
                sn = session.get('pos')
            else:
                se = request.form.get('pos').strip()
                session['pos'] = se
                qu = Acup.query.filter(or_( Acup.acpu_function.contains(session.get('pos')),
                                            Acup.acpu_indications.contains(session.get('pos')))).order_by("acup_name").all()
                sn = session.get('pos')
    if session['pos'] == False:
        qu = Mer.query.order_by("merd_name").all()
        sn = "十二經脈與經外奇穴"
    
    return render_template('encyclopedia.html',
                            qu=qu,
                            sn=sn)

@app.route('/LU',methods=['GET','POST'])
def LU():    
    
    return render_template('LU.html')

@app.route('/BL',methods=['GET','POST'])
def BL():    
    
    return render_template('BL.html')

@app.route('/CHONG',methods=['GET','POST'])
def CHONG():    
    
    return render_template('CHONG.html')

@app.route('/DAI',methods=['GET','POST'])
def DAI():    
    
    return render_template('DAI.html')

@app.route('/DU',methods=['GET','POST'])
def DU():    
    
    return render_template('DU.html')

@app.route('/GB',methods=['GET','POST'])
def GB():    
    
    return render_template('GB.html')

@app.route('/HT',methods=['GET','POST'])
def HT():    
    
    return render_template('HT.html')

@app.route('/KI',methods=['GET','POST'])
def KI():    
    
    return render_template('KI.html')

@app.route('/LI',methods=['GET','POST'])
def LI():    
    
    return render_template('LI.html')

@app.route('/LR',methods=['GET','POST'])
def LR():    
    
    return render_template('LR.html')

@app.route('/PC',methods=['GET','POST'])
def PC():    
    
    return render_template('PC.html')

@app.route('/RN',methods=['GET','POST'])
def RN():    
    
    return render_template('RN.html')

@app.route('/SI',methods=['GET','POST'])
def SI():    
    
    return render_template('SI.html')

@app.route('/SJ',methods=['GET','POST'])
def SJ():    
    
    return render_template('SJ.html')

@app.route('/SP',methods=['GET','POST'])
def SP():    
    
    return render_template('SP.html')

@app.route('/ST',methods=['GET','POST'])
def ST():    
    
    return render_template('ST.html')

@app.route('/WAQ',methods=['GET','POST'])
def WAQ():    
    
    return render_template('WAQ.html')

@app.route('/YAW',methods=['GET','POST'])
def YAW():    
    
    return render_template('YAW.html')

@app.route('/YIQ',methods=['GET','POST'])
def YIQ():    
    
    return render_template('YIQ.html')

@app.route('/YIW',methods=['GET','POST'])
def YIW():    
    
    return render_template('YIW.html')

@app.route('/BL1',methods=['GET','POST'])
def BL1():    
    
    return render_template('BL01.html')

@app.route('/DU1',methods=['GET','POST'])
def DU1():    
    
    return render_template('DU01.html')

@app.route('/Gb1',methods=['GET','POST'])
def Gb1():    
    
    return render_template('GB01.html')

@app.route('/HT1',methods=['GET','POST'])
def HT1():    
    
    return render_template('HT01.html')

@app.route('/KI1',methods=['GET','POST'])
def KI1():    
    
    return render_template('KI01.html')

@app.route('/LI1',methods=['GET','POST'])
def LI1():    
    
    return render_template('LI01.html')

@app.route('/LI11',methods=['GET','POST'])
def LI11():    
    
    return render_template('LI11.html')

@app.route('/LR1',methods=['GET','POST'])
def LR1():    
    
    return render_template('LR01.html')

@app.route('/LU1',methods=['GET','POST'])
def LU1():    
    
    return render_template('LU01.html')

@app.route('/Pc1',methods=['GET','POST'])
def Pc1():    
    
    return render_template('PC01.html')

@app.route('/Rn1',methods=['GET','POST'])
def Rn1():    
    
    return render_template('RN01.html')

@app.route('/SI1',methods=['GET','POST'])
def SI1():    
    
    return render_template('SI01.html')

@app.route('/SJ1',methods=['GET','POST'])
def SJ1():    
    
    return render_template('SJ01.html')

@app.route('/SP1',methods=['GET','POST'])
def SP1():    
    
    return render_template('SP01.html')

@app.route('/St1',methods=['GET','POST'])
def St1():    
    
    return render_template('ST01.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)















