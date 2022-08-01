# -- coding: utf-8 --
from apscheduler.schedulers.blocking import BlockingScheduler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from string import Template
from path import Path 



def mail():
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "test"  #郵件標題
    content["from"] = "108111113@mail.aeust.edu.tw"  #寄件者
    content["to"] = "108111113@mail.aeust.edu.tw" #收件者
    body = "123"
    content.attach(MIMEText(body))
    with smtplib.SMTP(host="smtp.office365.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("108111113@mail.aeust.edu.tw", "timmy279!")  # 
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)
            
mail()