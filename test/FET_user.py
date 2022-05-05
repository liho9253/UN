from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"

db = SQLAlchemy(app)

class User(db.Model):
    
    __tablename__ = 'Users'

    ID = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.String(20))
    EndDate = db.Column(db.String(20))
    Sub = db.Column(db.String(999))
    SpN = db.Column(db.String(20))
    CloseDate = db.Column(db.String(20))
    CreWGro = db.Column(db.String(90))
    SR = db.Column(db.String(90))
    CoxT = db.Column(db.String(90))
    Dec = db.Column(db.String(999))
    CreN = db.Column(db.String(20))

    def __init__(self, ID, StartDate, EndDate, Sub, SpN, CloseDate, CreWGro, SR, CoxT, Dec, CreN):
        self.ID = ID
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.Sub = Sub
        self.SpN = SpN
        self.CloseDate = CloseDate
        self.CreWGro = CreWGro
        self.SR = SR
        self.CoxT = CoxT
        self.Dec = Dec
        self.CreN = CreN
    def __repr__(self):
        return '<User %r>' % self.ID
    
if __name__ == "__main__":
    db.create_all()