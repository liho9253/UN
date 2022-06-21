import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

# os.environ['http_proxy'] = "http://127.0.0.1"
# os.environ['https_proxy'] = "https://127.0.0.1"
sender = 'from@gmail.com'
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

# import smtplib
# from email.mime.text import MIMEText 
# smtpHost = 'smtp.exmail.qq.com' 
# sender = '<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="dfadb0bdb0ab9fb2b6b2a9aff1bcb0b2">[email protected]</a>' 
# password = "mimvp-password" 
# receiver = '<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="7f061e1118181e11183f121612090f511c1012">[email protected]</a>'
# content = 'hello mimvp.com' 
# msg = MIMEText(content) 
# msg['Subject'] = 'email-subject' 
# msg['From'] = sender 
# msg['To'] = receiver 
   

## smtp port 25
smtpServer = smtplib.SMTP(smtpHost, 25)         # SMTP
smtpServer.login(sender, password) 
smtpServer.sendmail(sender, receiver, msg.as_string()) 
smtpServer.quit() 
print('send success by port 25' )
 
## smtp ssl port 465
smtpServer = smtplib.SMTP_SSL(smtpHost, 465)    # SMTP_SSL
smtpServer.login(sender, password) 
smtpServer.sendmail(sender, receiver, msg.as_string()) 
smtpServer.quit() 
print('send success by port 465' )




