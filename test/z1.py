from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/Test_farP"

db = SQLAlchemy(app)

class Model(db.Model):
    __tablename__ = 'Test_farP'

    id = db.Column(db.Integer, primary_key=True)
    ID = db.Column(db.String(90))
    Start = db.Column(db.String(90))
    End = db.Column(db.String(90))
    SpN = db.Column(db.String(90))

    def __init__(self, ID, Start, End, SpN):
        self.ID = ID
        self.Start = Start
        self.End = End
        self.SpN = SpN

    



if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
    
    
    
    
    