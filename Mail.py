import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

# MIME 문서를 생성합니다.
#htmlFD = open('htmlFileName', 'rb')
#HtmlPart = MIMEText(htmlFD.read(),'html', _charset = 'UTF-8' )
#htmlFD.close()

# 만들었던 mime을 MIMEBase에 첨부 시킨다.
#msg.attach(HtmlPart)

# 메일을 발송한다.

class MailSender:
    host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
    port = "587"

    def __init__(self, sendAddr, recipAddr, passwd, connection):
        self.senderAddr    = "scoke0801@gmail.com"     # 보내는 사람 email 주소.
        self.recipientAddr = "scoke0801@daum.net"   # 받는 사람 email 주소.
        self.connection = connection
        #self.senderAddr =  sendAddr # 보내는 사람 email 주소.
        #self.recipientAddr = recipAddr  # 받는 사람 email 주소.

    def OnCreate(self):
        self.msg = MIMEBase("multipart", "alternative")
        self.msg['Subject'] = "Test email in Python 3.6"
        self.msg['From'] = self.senderAddr
        self.msg['To'] = self.recipientAddr

    def OnDestroy(self):
        del self.msg

    def AddHTML(self, htmlText):
        self.HtmlPart = MIMEText(htmlText, 'html', _charset='UTF-8')

    def ConnectHTML(self):
        self.msg.attach(self.HtmlPart)

    def MakeHtmlDoc(self):
        from xml.dom.minidom import getDOMImplementation
        # get Dom Implementation
        impl = getDOMImplementation()

        newdoc = impl.createDocument(None, "html", None)  # DOM 객체 생성
        top_element = newdoc.documentElement
        header = newdoc.createElement('header')
        top_element.appendChild(header)

        # Body 엘리먼트 생성.
        body = newdoc.createElement('body')

        l = ["1234", "the book"]
        for bookitem in l:  # l - > booklist
            # create bold element
            b = newdoc.createElement('b')
            # create text node
            ibsnText = newdoc.createTextNode("ISBN:" + bookitem[0])
            b.appendChild(ibsnText)

            body.appendChild(b)

            # BR 태그 (엘리먼트) 생성.
            br = newdoc.createElement('br')

            body.appendChild(br)

            # create title Element
            p = newdoc.createElement('p')
            # create text node
            titleText = newdoc.createTextNode("Title:" + bookitem[1])
            p.appendChild(titleText)

            body.appendChild(p)
            body.appendChild(br)  # line end

        # append Body
        top_element.appendChild(body)

        return newdoc.toxml()
    def Send(self):
        self.OnCreate()

        print(self.connection.getData())
"""
        self.ConnectHTML()

        s = smtplib.SMTP(MailSender.host, MailSender.port)
        # s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("scoke0801@gmail.com", "dla753156")
        s.sendmail(self.senderAddr, [self.recipientAddr], self.msg.as_string())
        s.close()

        self.OnDestroy()
"""