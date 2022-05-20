from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(    
    MAIL_SERVER='timmy89566@gmail.com',
    MAIL_PROT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='曾偉國',
    MAIL_PASSWORD='as785241963')

mail = Mail(app)

@app.route("/message")
def index():
    msg_title = "Test"
    msg_sender = "曾偉國 timmy89566@gmail.com"
    msg_recipients = ['timmy89566@gmail.com']
    msg_body = "測試"
    
    msg = Message(msg_title,
                  sender=msg_sender,
                  recipients=msg_recipients)
    msg.body = msg_body

    mail.send(msg)
    return 'You Send Mail by Flask-Mail Success!!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
    
    
    
