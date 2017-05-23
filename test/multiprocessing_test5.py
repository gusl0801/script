from multiprocessing import Process, Queue
import time

class Simple:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)

def do_work(start, end, result):
    i = start
    for _ in range(start, end):
        s = Simple(i)
        result.put(s)
        print(i)
        i += 1
        time.sleep(0.1)
    print("for end")
    return

s_time = time.time()

if __name__=='__main__':
    START, END = 0, 100
    result = Queue()

    print(START, int(END/2), END)

    process_list =[]
    process_list.append(Process(target=do_work, args=(START, int(END/2), result)))
    process_list.append(Process(target=do_work, args=(int(END/2), END, result)))

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()

    result.put('STOP')
    count = 0
    while True:
        data = result.get()
        if data == 'STOP':
            break
        else:
            print("data", data, 'time =', time.time() - s_time, "count", count)
            count += 1
