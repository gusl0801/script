from XMLBook import *
from http.client import HTTPConnection
import requests
from multiprocessing import Process, Queue
import urllib

conn = None
#regKey = '1ckRGPeUTj7n2EeO5dyg6aaV8FOMSVfUr%2FRc%2Bsp47rkQ8dqRTygAs3vZoJ%2BZ%2B%2BvkBJDqmHZh9lgOrNq%2FlEN6jQ%3D%3D'
regKey = 'vFv%2BD0ZVc6q%2BHgQYvvUdYWFhq2D%2BOdeV9H%2BVfeGtfaeBFTmw1rtrBNPFL2bQGAOSgDwzh1gqpzv7zh2QwXxHkA%3D%3D'
'fCsP7thL6aSOrQGp0mrFUKF3r09CsgzFVMKwS8CVPDeYjSRJb263KAriJp7ihE5g7lA5r1eRkbE6fzNrkQQw6g%3D%3D'

'ayXwapYyvKNjpOaOMxDeepxLGpnXBsJ96L51RvkgKiTBxpZRhaJBrrcbrXRcPkimlVNFd7BiqTee4ZX5VFJyIQ%3D%3D'
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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    hangul_utf8 = urllib.parse.quote(title)
    uri = URIBuilder(server, serviceKey =regKey,
                     title = hangul_utf8,
                     manageCd = "MA")
                     #numOfRows = '5',
                     #pageNo = '5',
                     #startPage = '2')

    req = requests.get(uri, headers=headers)
    if int(req.status_code) == 200:
        print("Book data downloading complete!")
        retData = XMLBook()
        retData.LoadFromText(req.content)
        return retData
    else:
        print("OpenAPI request has been failed!! please retry")
        return None
    """
    testList = []

    for i in range(len(libCodeList)):
        uri = URIBuilder(server, serviceKey = regKey,
                         title = title,
                         manageCd = libCodeList[i])
        req = requests.get(uri, headers = headers)

        if int(req.status_code) is not 200:
            continue

        testList.append(XMLBook())
        testList[i].LoadFromText(req.content)
    return testList
    """

def ProcessFunc(start, end, result, keyword):
    global server, regKey, conn

    if conn == None:
        connectOpenAPIServer()

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    keyword = urllib.parse.quote(keyword)

    i = start
    for _ in range(start, end):
        uri = URIBuilder(server, serviceKey=regKey,
                         title= keyword,
                         manageCd=libCodeList[i])

        req = requests.get(uri, headers=headers)
        print(req.raw)
        print(req.content)
        if req.status_code is 200:
            data = XMLBook()
            data.LoadFromText(req.content)
            result.put(XMLBook())

        print(i)
        i += 1
    print("for end")
    return

def getBookData(searchTag):
    START, END = 0, len(libCodeList)
    result = Queue()

    print(START, int(END / 2), END)

    process_list = []

    process_list.append(Process(target=ProcessFunc, args=(START, int(END / 4 * 1), result)))
    process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 1), int(END / 4 * 2), result)))
    process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 2), int(END / 4 * 3), result)))
    process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 3), END, result)))

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()

    result.put('STOP')
    print("result size", result.qsize())

    while True:
        data = result.get()
        if data == 'STOP':
            break
        else:
            data.PrintBookList()
