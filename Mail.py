import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import spam

# MIME 문서를 생성합니다.
#htmlFD = open('htmlFileName', 'rb')
#HtmlPart = MIMEText(htmlFD.read(),'html', _charset = 'UTF-8' )
#htmlFD.close()

# 만들었던 mime을 MIMEBase에 첨부 시킨다.
#msg.attach(HtmlPart)

# 메일을 발송한다.
xmlText = '<?xml version="1.0" ?>\
            <booklist cnt="3">\
            <book ISBN="0399250395">\
            <title>The Very Hungry Caterpillar Pop-Up Book</title>\
            <author name="Eric Carle"/>\
            <author name="Keith Finch"/>\
            <publisher> Philomel Books</publisher>\
            <description> Celebrating the 40th anniverary of one of the most popular children s books ever created</description>\
            </book>\
            <book ISBN="0964729237">\
            <title lang="english">The Shack</title>\
            </book>\
            <book ISBN="0553281097">\
            <title>You Can Negotiate Anything</title>\
            <author name="Herb Cohen"/>\
            <category cid="12">Negotiate and narrative skill</category>\
            </book>\
            </booklist>'

class MailSender:
    host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
    port = "587"

    def __init__(self, sendAddr, recipAddr, passwd, connection, entry):
        self.senderAddr    = "scoke0801@gmail.com"     # 보내는 사람 email 주소.
        self.recipientAddr = "scoke0801@daum.net"   # 받는 사람 email 주소.
        self.connection = connection
        self.entry = entry
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

    def AddXML(self, xmlText):
        self.XMLPart =  MIMEText(xmlText, 'xml', _charset = "UTF-8")

    def ConnectHTML(self):
        self.msg.attach(self.HtmlPart)

    def ConnectXML(self):
        self.msg.attach(self.XMLPart)

    def MakeHtmlDoc(self, bookList):
        from xml.dom.minidom import getDOMImplementation
        # get Dom Implementation
        impl = getDOMImplementation()

        newdoc = impl.createDocument(None, "html", None)  # DOM 객체 생성
        top_element = newdoc.documentElement
        header = newdoc.createElement('header')
        top_element.appendChild(header)

        # Body 엘리먼트 생성.
        body = newdoc.createElement('body')
# ---------------------------------------------
        # create bold element
        b = newdoc.createElement('b')
        # create text node
        for text in bookList:
            if spam.findStr(text, "title") != 0:
                #"isbn" + " : "
                print("in title : ", text)
                titleText = newdoc.createTextNode("TITLE:" + text[8:])
                b.appendChild(titleText)
                body.appendChild(b)
                break

        # BR 태그 (엘리먼트) 생성.
        br = newdoc.createElement('br')

        body.appendChild(br)

        # create title Element
        p = newdoc.createElement('p')
        # create text node
        for text in bookList:
            if spam.findStr(text, "isbn") != 0:
                print("in isbn : ", text)
                isbnText = newdoc.createTextNode("ISBN:" + text[7:])
                p.appendChild(isbnText)
                body.appendChild(p)
                break

        p = newdoc.createElement('p')

        for text in bookList:
            if spam.findStr(text, "author") != 0:
                print("in author : ", text)
                authorText = newdoc.createTextNode("Author:" + text[9:])
                p.appendChild(authorText)
                body.appendChild(p)
                break


        for text in bookList:
            if spam.findStr(text, "libName") != 0:
                print("in libName : ", text)
                authorText = newdoc.createTextNode("LibName:" + text[10:])
                p.appendChild(authorText)
                body.appendChild(p)
                break

        body.appendChild(br)  # line end
#---------------------------------------------
        # append Body
        top_element.appendChild(body)

        return newdoc.toxml()

    def Send(self):
        self.recipientAddr = self.entry.get()
        print(self.recipientAddr)

        self.OnCreate()

        html = self.MakeHtmlDoc(self.connection.getListData())
        self.AddHTML(html)
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

if __name__ == '__main__':
    result = MIMEText(xmlText, 'xml', _charset="UTF-8")
    print(result)