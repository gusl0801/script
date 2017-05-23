from multiprocessing import Process, Lock, Value
import time

from XMLBook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

conn = None
regKey = '1ckRGPeUTj7n2EeO5dyg6aaV8FOMSVfUr%2FRc%2Bsp47rkQ8dqRTygAs3vZoJ%2BZ%2B%2BvkBJDqmHZh9lgOrNq%2FlEN6jQ%3D%3D'

server = 'openapi-lib.sen.go.kr'
libCodeList = ['MA', 'MB', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MV', 'MJ', 'MK', 'ML',
               'MX', 'MM', 'MP', 'MW', 'MN', 'MQ', 'MR', 'MS', 'MT', 'MU']
index = 0
testList = []
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
    # print(itemElements)
    for item in itemElements:
        isbn = item.find("isbn")
        strTitle = item.find("title")
        print(strTitle.text)
        if len(strTitle.text) > 0:
            return {"ISBN": isbn.text, "title": strTitle.text}


def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)


def getBookDataFromTitle(title):
    global server, regKey, conn
    if conn == None:
        connectOpenAPIServer()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    uri = URIBuilder(server, serviceKey=regKey,
                     title=title,
                     manageCd="MA")
    # numOfRows = '5',
    # pageNo = '5',
    # startPage = '2')

    testList = []

    for i in range(len(libCodeList)):
        uri = URIBuilder(server, serviceKey=regKey,
                         title=title,
                         manageCd=libCodeList[i])
        req = requests.get(uri, headers=headers)

        if int(req.status_code) is not 200:
            continue

        testList.append(XMLBook())
        testList[i].LoadFromText(req.content)
    return testList

def run(name, l, c):
    global server, regKey, conn, index, testList

    if conn == None:
        connectOpenAPIServer()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

    print(name, "process is created.")

    while 1:
        l.acquire()
        if c.value > 0:
            c.value -= 1
            l.release()
            uri = URIBuilder(server, serviceKey=regKey,
                             title= "도둑",
                             manageCd=libCodeList[index])
            req = requests.get(uri, headers=headers)

            if int(req.status_code) is 200:
                testList.append(XMLBook())
                testList[index].LoadFromText(req.content)
                print(req.raw)
                print(testList[index])
                print(index)

            index += 1
            #time.sleep(0.01)
        else:
            l.release()
            print(name, "index", index, "processed")
            break


if __name__ == '__main__':
    lock = Lock()
    count = Value('i',22)

    dev_list = []
    for name in ['Shin', 'Woo', 'Choi']:
        dev = Process(target = run, args =(name,lock,count))
        dev_list.append(dev)
        dev.start()

    for dev in dev_list:
        dev.join()
    print('All processes are finished', index, len(testList))
    for data in testList:
        print(data)