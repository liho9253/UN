# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user_name:password@IP:5432/db_name"

db = SQLAlchemy()
db.init_app(app)

@app.route('/')
@app.route('/table')
def table():
    df = pd.read_csv("./SR-Sample.csv", encoding="utf-8")
    df=df.dropna()
    df.index+=1
    data_html=df[0:].to_html()
    titles = ["None", "Job List"]
    return render_template('table_raw.html', tables=[data_html], titles=titles)
  
  
if __name__ == "__main__":
    """
        export FLASK_APP=fet_main.py
        export FLASK_ENV=fet_develop
        flask run
    """
    app.run(host="localhost", port=5000, debug=True)
