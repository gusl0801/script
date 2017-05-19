from XMLBook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer


conn = None
regKey = '1ckRGPeUTj7n2EeO5dyg6aaV8FOMSVfUr%2FRc%2Bsp47rkQ8dqRTygAs3vZoJ%2BZ%2B%2BvkBJDqmHZh9lgOrNq%2FlEN6jQ%3D%3D'

server = 'openapi-lib.sen.go.kr'

"""
'http://openapi-lib.sen.go.kr' \
'/openapi/service/lib/openApi' \
'?serviceKey=1ckRGPeUTj7n2EeO5dyg6aaV8FOMSVfUr%2FRc%2Bsp47rkQ8dqRTygAs3vZoJ%2BZ%2B%2BvkBJDqmHZh9lgOrNq%2FlEN6jQ%3D%3D
&title=%EB%8F%84%EB%91%91' \
'&manageCd=MB' \
'&numOfRows=5' \
'&pageSize=5' \
'&pageNo=2' \
'&startPage=2'
"""
def URIBuilder(server, **user):
    str = "https://" + server + "/openapi/service/lib/openApi?"

    for key in user.keys():
        str += key + '=' + user[key] + '&'
    return 'http://openapi-lib.sen.go.kr' \
'/openapi/service/lib/openApi' \
'?serviceKey=1ckRGPeUTj7n2EeO5dyg6aaV8FOMSVfUr%2FRc%2Bsp47rkQ8dqRTygAs3vZoJ%2BZ%2B%2BvkBJDqmHZh9lgOrNq%2FlEN6jQ%3D%3D\
&title=%EB%8F%84%EB%91%91' \
'&manageCd=MB' \
'&numOfRows=5' \
'&pageSize=5' \
'&pageNo=2' \
'&startPage=2'
    # return str

def extractBookData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    print (strXml)
    # Book 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("item")  # return list type
    print(itemElements)
    for item in itemElements:
        isbn = item.find("isbn")
        strTitle = item.find("title")
        print (strTitle)
        if len(strTitle.text) > 0 :
           return {"ISBN":isbn.text,"title":strTitle.text}

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)
    aa = 1

def getBookDataFromTitle(title):
    global server, regKey, conn
    if conn == None:
        connectOpenAPIServer()
    # uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)
    uri = URIBuilder(server, apikey=regKey, manageCd = "MB", numOfRows = '5', pageNo = '5')
    conn.request("GET", 'http://openapi-lib.sen.go.kr' \
'/openapi/service/lib/openApi' \
'?serviceKey=1ckRGPeUTj7n2EeO5dyg6aaV8FOMSVfUr%2FRc%2Bsp47rkQ8dqRTygAs3vZoJ%2BZ%2B%2BvkBJDqmHZh9lgOrNq%2FlEN6jQ%3D%3D\
&title=%EB%8F%84%EB%91%91' \
'&manageCd=MB' \
'&numOfRows=5' \
'&pageSize=5' \
'&pageNo=2' \
'&startPage=2')

    req = conn.getresponse()
    print(req.status)

    if int(req.status) == 200:
        print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print("OpenAPI request has been failed!! please retry")
        return None