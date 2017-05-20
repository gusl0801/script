from XMLBook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

MAX_RETRIES = 20

conn = None
regKey = '1ckRGPeUTj7n2EeO5dyg6aaV8FOMSVfUr%2FRc%2Bsp47rkQ8dqRTygAs3vZoJ%2BZ%2B%2BvkBJDqmHZh9lgOrNq%2FlEN6jQ%3D%3D'

server = 'openapi-lib.sen.go.kr'

"""
'http://openapi-lib.sen.go.kr' \
'/openapi/service/lib/openApi
?serviceKey=1ckRGPeUTj7n2EeO5dyg6aaV8FOMSVfUr%2FRc%2Bsp47rkQ8dqRTygAs3vZoJ%2BZ%2B%2BvkBJDqmHZh9lgOrNq%2FlEN6jQ%3D%3D
&title=%EB%8F%84%EB%91%91' \
'&manageCd=MB' \
'&numOfRows=5' \
'&pageSize=5' \
'&pageNo=2' \
'&startPage=2'
"""

"""
http://openapi-lib.sen.go.kr/openapi/service/lib/openApi
?serviceKey=1ckRGPeUTj7n2EeO5dyg6aaV8FOMSVfUr%2FRc%2Bsp47rkQ8dqRTygAs3vZoJ%2BZ%2B%2BvkBJDqmHZh9lgOrNq%2FlEN6jQ%3D%3D
&title=%EB%8F%84%EB%91%91
&manageCd=MB
&numOfRows=5
&pageSize=5
&pageNo=2
&startPage=2
"""
def URIBuilder(server, **user):
    str = "http://" + server + "/openapi/service/lib/openApi?"

    for key in user.keys():
        str += key + '=' + user[key] + '&'
    return str

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
                     title = '%EB%8F%84%EB%91%91',
                     manageCd = "MB",
                     numOfRows = '5',
                     pageNo = '5',
                     startPage = '2')
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

    print(req.status_code)

    if int(req.status_code) == 200:
        print("Book data downloading complete!")
        #return extractBookData(req.read())
        return extractBookData(req.content)
    else:
        print("OpenAPI request has been failed!! please retry")
        return None