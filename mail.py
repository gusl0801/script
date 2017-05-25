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