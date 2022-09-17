from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3306/fet"

ad_db = SQLAlchemy(app)

class AD(ad_db.Model):
    
    __tablename__ = 'AD'

    Name = ad_db.Column(ad_db.String(64), primary_key=True)
    Mail = ad_db.Column(ad_db.String(64))
    PassWord = ad_db.Column(ad_db.String(64))
    Permission = ad_db.Column(ad_db.String(1))

    def __init__(self, Name, Mail, PassWord, Permission):
        self.Name = Name
        self.Mail = Mail
        self.PassWord = PassWord
        self.Permission = Permission
    def __repr__(self):
        return '<AD %r>' % self.Name
    
if __name__ == "__main__":
    ad_db.create_all()