import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'timmy89566@gmail.com'
receivers = ['timmy89566@gmail.com']

message = """
This is a test e-mail message.
sssddd
"""

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message)         
   print("Successfully sent email")
except Exception:
   print ("Error: unable to send email")