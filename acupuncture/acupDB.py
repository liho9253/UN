from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.urandom(24)

adb = SQLAlchemy(app)

class Acup(adb.Model):
    
    __tablename__ = 'Acup'

    merd_id = adb.Column(adb.String(4))
    acup_id = adb.Column(adb.String(8), primary_key=True)
    acup_name = adb.Column(adb.String(16))
    acup_enname = adb.Column(adb.String(32))
    acup_alias = adb.Column(adb.String(256))
    acup_take = adb.Column(adb.String(128))
    acpu_acupuncture = adb.Column(adb.String(8))
    acpu_function = adb.Column(adb.String(128))
    acpu_indications = adb.Column(adb.String(128))

    def __init__(self, merd_id, acup_id, acup_name, acup_enname, acup_alias, acup_take, acpu_acupuncture, acpu_function, acpu_indications):
        self.merd_id = merd_id
        self.acup_id = acup_id
        self.acup_name = acup_name
        self.acup_enname = acup_enname
        self.acup_alias = acup_alias
        self.acup_take = acup_take
        self.acpu_acupuncture = acpu_acupuncture
        self.acpu_function = acpu_function
        self.acpu_indications = acpu_indications
    def __repr__(self):
        return '<Acup %r>' % self.acup_id
    
if __name__ == "__main__":
    adb.create_all()