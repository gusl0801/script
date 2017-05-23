from InternetBook import *

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
    return result

if __name__ == '__main__':
    result = getBookData(1)

    while True:
        elem = result.get()
        if elem == 'STOP':
            break
        else:
            elem.PrintBookList()
