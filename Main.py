from OpenAPIServer import *
from Interface import*
from multiprocessing import Pool
from DaumAPIServer import *

def LibSearchSimpleHandler(title, lib_code):
    content = ProcessFuncSimple(title, lib_code)
    book = XMLBook(api='data')
    book.LoadFromText(content)
    book.PrintBookList()

    retList = [book]
    return retList


def LibSearchButtonHandler(title):
    textList = getBookDataPool(title)
    #print("-----------------------get text queue data-----------------------")
    bookList = []

    #if len(textList) is not 0:
    #    print("검색이 완료 되었습니다!", len(textList))
    #else:
    #    print("검색 결과가 없습니다 ㅜ.ㅜ")

        # PrintMenu()
    for i in range(len(textList)):
        for j in range(len(textList[i])):
            book = XMLBook(api='data')
            book.LoadFromText(textList[i][j])
            book.PrintBookList()
            bookList.append(book)
    #print("검색 결과 : ", len(bookList))
    if len(bookList) != 0:
       return bookList
    return None

def getBookData(searchTag):
    START, END = 0, len(libCodeList)
    result = Queue()
    # print(START, int(END / 2), END)

    process_list = []
    #process_list.append(Process(target=ProcessFunc, args=(0, 1, result, '도둑')))
    process_list.append(Process(target=ProcessFunc, args=(START, int(END / 4 * 1), result, searchTag)))
    process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 1), int(END / 4 * 2), result, searchTag)))
    #process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 2), int(END / 4 * 3), result, searchTag)))
    #process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 3), END, result, searchTag)))

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()

    result.put('STOP')
    return result

def getBookDataL(searchTag):
    START, END = 0, len(libCodeList)
    RANGE = 1
    queueList = [Queue() for _ in range(RANGE)]
    result = Queue()
    # print(START, int(END / 2), END)

    process_list = []
    #process_list.append(Process(target=ProcessFunc, args=(0, 1, queueList, '도둑')))
    process_list.append(Process(target=ProcessFunc, args=(START, int(END / 4 * 1), queueList[0], searchTag)))
    process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 1), int(END / 4 * 2), queueList[1], searchTag)))
    process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 2), int(END / 4 * 3), queueList[2], searchTag)))
    process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 3), END, queueList[3], searchTag)))

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()

    print ("get data")
    for i in range(RANGE):
        while queueList[i].qsize() > 0:
            result.put(queueList[i].get())

    print("result.size", result.qsize())

    result.put('STOP')

    return result

def getBookDataPool(searchTag):
    START, END = 0, len(libCodeList)
    paramaters =\
    [
        (START, int(END / 4 * 1), searchTag),
        (int(END / 4 * 1), int(END / 4 * 2), searchTag),
        (int(END / 4 * 2), int(END / 4 * 3), searchTag),
        (int(END / 4 * 3), END, searchTag)
    ]

    pool = Pool(processes=4)
    result = pool.starmap(PoolFunc, paramaters)

    pool.close()
    pool.join()
    return result

if __name__ == '__main__':
    interface = InterfaceManager(title ="소장도서 검색기", pos ='480x640+300+100')
    interface.AllCreates()
    interface.AllRegist()

    interface.StartLoop()
    """
    while True:
    
        # keyword = GetKeyword()
        # textQueue = getBookDataL('도둑')
        textList = getBookDataPool('도둑')
        print("-----------------------get text queue data-----------------------")
        bookList = []

        
        if len(textList) is not 0:
            print("검색이 완료 되었습니다!", len(textList))
        else:
            print("검색 결과가 없습니다 ㅜ.ㅜ")
            print("재진행 합니다")
            continue

        # PrintMenu()
        for i in range(len(textList)):
            for j in range(len(textList[i])):
                book = XMLBook(api='data')
                book.LoadFromText(textList[i][j])
                book.PrintBookList()
                bookList.append(book)
        print("검색 결과 : ",len(bookList))
        
        break
"""

"""
        while True:
            elem = textQueue.get()
            if elem == 'STOP':
                break
            else:
                book = XMLBook(api='data')
                book.LoadFromText(elem)
                book.PrintBookList()
                bookList.append(book)
        print("최종 결과 크기", len(bookList))
        """
"""
        START, END = 0, len(libCodeList)

        textQueue = Queue()

        process_list = []
        #process_list.append(Process(target=ProcessFunc, args=(0, 1, result, keyword)))
        process_list.append(Process(target=ProcessFunc, args=(0, 1, textQueue, '도둑')))

        for process in process_list:
            process.start()

        for process in process_list:
            process.join()

        textQueue.put('STOP')
        """
"""
    result = getBookData("도둑")

    while True:
        elem = result.get()
        if elem == 'STOP':
            break
        else:
            elem.PrintBookList()

"""