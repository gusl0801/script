from XMLBook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from multiprocessing import Process, Queue
import time
conn = None
regKey = '1ckRGPeUTj7n2EeO5dyg6aaV8FOMSVfUr%2FRc%2Bsp47rkQ8dqRTygAs3vZoJ%2BZ%2B%2BvkBJDqmHZh9lgOrNq%2FlEN6jQ%3D%3D'

server = 'openapi-lib.sen.go.kr'
libCodeList = ['MA', 'MB', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MV', 'MJ', 'MK', 'ML',
               'MX', 'MM', 'MP', 'MW', 'MN', 'MQ', 'MR', 'MS', 'MT', 'MU']

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

def do_work(start, end, result):
    global server, regKey, conn, testL
    if conn == None:
        connectOpenAPIServer()
        pass
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

    i = start
    for _ in range(start, end):
        uri = URIBuilder(server, serviceKey=regKey,
                         title="도둑",
                         manageCd=libCodeList[i])

        req = requests.get(uri, headers=headers)

        if req.status_code is 200:
            data = XMLBook()
            data.LoadFromText(req.content)
            result.put(XMLBook())

        print(i)
        i += 1
    print("for end")
    return

s_time = time.time()

if __name__=='__main__':
    START, END = 0, len(libCodeList)
    result = Queue()

    print(START, int(END/2), END)

    process_list =[]
    process_list.append(Process(target=do_work, args=(START, int(END / 4 * 1), result)))
    process_list.append(Process(target=do_work, args=(int(END / 4 * 1), int(END / 4 * 2), result)))
    process_list.append(Process(target=do_work, args=(int(END / 4 * 2), int(END / 4 * 3), result)))
    process_list.append(Process(target=do_work, args=(int(END / 4 * 3), END, result)))

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
            print('time =', time.time() - s_time)

    print('time =', time.time() - s_time)
