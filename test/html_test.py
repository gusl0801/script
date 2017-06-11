def MakeHtmlDoc():
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
    for bookitem in l: # l - > booklist
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

if __name__ == '__main__':
    import smtplib
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    result = MakeHtmlDoc()

    host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
    port = "587"

    senderAddr = "scoke0801@gmail.com"  # 보내는 사람 email 주소.
    recipientAddr = "scoke0801@daum.net"  # 받는 사람 email 주소.

    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = "Test email in Python 3.6"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    HtmlPart = MIMEText(result, 'html', _charset='UTF-8')

    msg.attach(HtmlPart)

    s = smtplib.SMTP(host, port)
    # s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("scoke0801@gmail.com", "dla753156")
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()