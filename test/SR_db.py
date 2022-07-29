from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:timmy279@localhost:5432/postgres"

sr_db = SQLAlchemy(app)

class SR(sr_db.Model):
    
    __tablename__ = 'SR'

    Name = sr_db.Column(sr_db.String(64), primary_key=True)
    MVPN = sr_db.Column(sr_db.String(16))
    Mail = sr_db.Column(sr_db.String(64))

    def __init__(self, Name, MVPN, Mail):
        self.Name = Name
        self.MVPN = MVPN
        self.Mail = Mail
    def __repr__(self):
        return '<SR %r>' % self.Name
    
if __name__ == "__main__":
    sr_db.create_all()