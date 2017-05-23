from InternetBook import *
from Interface import*

def getBookData(searchTag):
    START, END = 0, len(libCodeList)
    result = Queue()

    print(START, int(END / 2), END)

    process_list = []

    process_list.append(Process(target=ProcessFunc, args=(START, int(END / 4 * 1), result, searchTag)))
    process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 1), int(END / 4 * 2), result, searchTag)))
    process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 2), int(END / 4 * 3), result, searchTag)))
    process_list.append(Process(target=ProcessFunc, args=(int(END / 4 * 3), END, result, searchTag)))

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()

    result.put('STOP')
    return result

if __name__ == '__main__':

    while True:
        keyword = GetKeyword()
        result = getBookData(keyword)

        if result.qsize() is not 0:
            print("검색이 완료 되었습니다!")
        else:
            print("검색 결과가 없습니다 ㅜ.ㅜ")
            print("재진행 합니다")
            continue

        PrintMenu()

        while True:
            elem = result.get()
            if elem == 'STOP':
                break
            else:
                elem.PrintBookList()
"""
    result = getBookData("도둑")

    while True:
        elem = result.get()
        if elem == 'STOP':
            break
        else:
            elem.PrintBookList()
"""