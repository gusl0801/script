from XMLBook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

conn = None
regKey = '1ckRGPeUTj7n2EeO5dyg6aaV8FOMSVfUr%2FRc%2Bsp47rkQ8dqRTygAs3vZoJ%2BZ%2B%2BvkBJDqmHZh9lgOrNq%2FlEN6jQ%3D%3D'

server = 'openapi-lib.sen.go.kr'
libCodeList = ['MA', 'MB', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MV', 'MJ', 'MK', 'ML',
               'MX', 'MM', 'MP', 'MW', 'MN', 'MQ', 'MR', 'MS', 'MT', 'MU']
"""
MA	강남도서관
MB	강동도서관
MC	강서도서관
MD	개포도서관
ME	고덕평생학습관
MF	고척도서관
MG	구로도서관
MH	남산도서관
MV	노원평생학습관
MJ	도봉도서관
MK	동대문도서관
ML	동작도서관
MX	마포평생아현분관
MM	마포평생학습관
MP	서대문도서관
MW	송파도서관
MN	양천도서관
MQ	어린이도서관
MR	영등포평생학습관
MS	용산도서관
MT	정독도서관
MU	종로도서관
"""
def URIBuilder(server, **user):
    str = "http://" + server + "/openapi/service/lib/openApi?"

    for key in user.keys():
        str += key + '=' + user[key] + '&'
    return str

def extractBookData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    # print (strXml)
    # Book 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("item")  # return list type
    #print(itemElements)
    for item in itemElements:
        isbn = item.find("isbn")
        strTitle = item.find("title")
        print(strTitle.text)
        if len(strTitle.text) > 0 :
           return {"ISBN":isbn.text,"title":strTitle.text}

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)

def getBookDataFromTitle(title):
    global server, regKey, conn
    if conn == None:
        connectOpenAPIServer()
    # uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)
    uri = URIBuilder(server, serviceKey =regKey,
                     title = '도둑',
                     manageCd = "MB",)
                     #numOfRows = '5',
                     #pageNo = '5',
                     #startPage = '2')
    # 기본 코드
    """
    conn.request("GET", uri)
    req = conn.getresponse()
    print(req.status)
    
    if int(req.status) == 200 :
        print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    req = requests.get(uri, headers=headers)

    if int(req.status_code) == 200:
        print("Book data downloading complete!")
        retData = XMLBook()
        retData.LoadFromText(req.content)
        return retData
        # return extractBookData(req.content)
    else:
        print("OpenAPI request has been failed!! please retry")
        return None
