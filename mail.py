"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# global value
host = "smtp.gmail.com"
port = "587"
password = ""
SENDER_ADDR = "scoke0801@gmail.com"
SENDER_PASSWD = ""
senderAddr = "scoke0801@gmail.com"
recipientAddr = None

# Message container를 생성합니다.
msg = MIMEMultipart('alternative')

# set message
msg["Title"] = "test message"
msg["From"] = senderAddr
msg["To"] = recipientAddr

msgPart = MIMEText("전송 텍스트", "plain")                   # 수정 필요
dataPart = MIMEText("전송 html", "html", _charset = "UTF-8") # 수정 필요

# Attach MIME to created msg
msg.attach(msgPart)
msg.attach(dataPart)

print("connect smtp server ... ")
s = smtplib.SMTP(host, port)
s.ehlo()
s.starttls()
s.ehlo()

s.login(senderAddr, password)
s.sendmail(senderAddr, [recipientAddr], msg.as_string())
s.close()

print("mail sending complete!")

class MailHandler:
    HOST = "smtp.gmail.com"
    PORT = "587"

    def __init__(self, recipientAddr = "scoke0801@daum.net"):
        # Message container를 생성합니다.
        self.msg = MIMEMultipart('alternative')

        self.senderAddr = SENDER_ADDR
        self.passwd = SENDER_PASSWD

        self.recipientAddr = recipientAddr

    def Send(self):
        pass
    
"""

# -*- coding: cp949 -*-
import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

#global value
host = "smtp.gmail.com" # Gmail STMP 서버 주소.
port = "587"
htmlFileName = "logo.html"

senderAddr = "scoke0801@gmail.com"     # 보내는 사람 email 주소.
recipientAddr = "scoke0801@daum.net"   # 받는 사람 email 주소.

msg = MIMEBase("multipart", "alternative")
msg['Subject'] = "Test email in Python 3.6"
msg['From'] = senderAddr
msg['To'] = recipientAddr

# MIME 문서를 생성합니다.
htmlFD = open(htmlFileName, 'rb')
HtmlPart = MIMEText(htmlFD.read(),'html', _charset = 'UTF-8' )
htmlFD.close()

# 만들었던 mime을 MIMEBase에 첨부 시킨다.
msg.attach(HtmlPart)

# 메일을 발송한다.
s = smtplib.SMTP(host,port)
#s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
s.ehlo()
s.starttls()
s.ehlo()
s.login("scoke0801@gmail.com","dla753156")
s.sendmail(senderAddr , [recipientAddr], msg.as_string())
s.close()