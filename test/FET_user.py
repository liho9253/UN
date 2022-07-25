from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"

db = SQLAlchemy(app)

class User(db.Model):
    
    __tablename__ = 'Users'

    ID = db.Column(db.String(10), primary_key=True)
    StartDate = db.Column(db.String(20))
    EndDate = db.Column(db.String(20))
    Sub = db.Column(db.String(999))
    SpN = db.Column(db.String(20))
    CreWGro = db.Column(db.String(90))
    SR = db.Column(db.String(90))
    CoxT = db.Column(db.String(90))
    CreN = db.Column(db.String(20))
    Major = db.Column(db.String(1))
    State = db.Column(db.String(20))

    def __init__(self, ID, StartDate, EndDate, Sub, SpN,  CreWGro, SR, CoxT, CreN, Major, State):
        self.ID = ID
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.Sub = Sub
        self.SpN = SpN
        self.CreWGro = CreWGro
        self.SR = SR
        self.CoxT = CoxT
        self.CreN = CreN
        self.Major = Major
        self.State = State
    def __repr__(self):
        return '<User %r>' % self.ID
    
if __name__ == "__main__":
    db.create_all()