# from threading import Thread
# from flask import Flask
# from flask_mail import Mail
# from flask_mail import Message

# app = Flask(__name__)
# app.config.update(
#     MAIL_SERVER='smtp.office365.com',
#     MAIL_PROT=587,
#     MAIL_USE_TLS=True,
#     MAIL_USERNAME='smtp-mail.outlook.com',
#     MAIL_PASSWORD='STARTTLS'
# )
# mail = Mail(app)


# @app.route("/message")
# def index():
#     msg_title = 'Hello It is Flask-Mail'
#     msg_sender = 'timmy89566@gmail.com'
#     msg_recipients = ['timmy89566@gmail.com']
#     msg_body = 'Hey, I am mail body!'
#     msg = Message(msg_title,
#                   sender=msg_sender,
#                   recipients=msg_recipients)
#     msg.body = msg_body

#     mail.send(msg)
#     return 'You Send Mail by Flask-Mail Success!!'

# if __name__ == "__main__":
#     app.debug = True
#     app.run()

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

os.environ['http_proxy'] = "http://127.0.0.1"
os.environ['https_proxy'] = "https://127.0.0.1"
sender = 'from@runoob.com'
receivers = ['timmy89566@gmail.com']
message = MIMEText('Python 測試...', 'plain', 'utf-8')
message['From'] = Header("123", 'utf-8')   
message['To'] =  Header("測試", 'utf-8')     
 
subject = 'Python SMTP 測試'
message['Subject'] = Header(subject, 'utf-8')


smtpObj = smtplib.SMTP('localhost', 25)
smtpObj.sendmail(sender, receivers, message.as_string())
try:
    print("成功")
except smtplib.SMTPException:
    print("Error")




