def Search(**arg):
    pass

from http.client import HTTPConnection
import requests
from XMLBook import *
from xml.dom import minidom

##global
conn = None
regKey = 'a2fa7710b162d3210d99e177cc0a2b86'

server = "apis.daum.net"

# smtp 정보
host = "smtp.gmail.com"  # Gmail SMTP 서버 주소.
port = "587"

def userURIBuilder(server, **user):
    # str = "http://" + server + "/search" + "?"
    str = "https://" + server + "/search/book" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)

def getBookData(query, keyword):
    global server, regKey, conn
    if conn == None:
        connectOpenAPIServer()
    # uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)
    uri = userURIBuilder(server, apikey=regKey, q=keyword, output="xml", sort = 'accu', result = '20', pageNo = '3')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

    req = requests.get(uri, headers = headers)

    if req.status_code == 200:
        b = XMLBook(api = 'daum')
        b.LoadFromText(req.content)
        result = b.SearchBooks(query = query, keyword = keyword)

        print("Book data downloading complete!")
        return result
    else:
        print("OpenAPI request has been failed!! please retry")
        return None


def extractBookData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    print(strXml)
    # Book 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("item")  # return list type
    print(itemElements)
    for item in itemElements:
        isbn = item.find("isbn")
        strTitle = item.find("title")
        print(strTitle)
        if len(strTitle.text) > 0:
            return {"ISBN": isbn.text, "title": strTitle.text}

def checkConnection():
    global conn
    if conn == None:
        print("Error : connection is fail")
        return False
    return True

if __name__ == '__main__':
    isbn = '0596513984'
    getBookData(isbn)