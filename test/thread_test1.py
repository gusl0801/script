from threading import Thread, Lock
import time

count = 10
lock = Lock()

class developer(Thread):
    def __init__(self,name):
        Thread.__init__(self)
        self.name = name
        self.fixed = 0
    def run(self):
        global count
        while 1:
            lock.acquire()  # lock
            if count > 0:
                count -= 1
                lock.release()  # unlock
                self.fixed += 1
                time.sleep(0.1)
            else:
                lock.release()  # unlock
                break

dev_list = []
for name in ['Shin', "Woo", "Choi"]:
    dev = developer(name)   # thread 생성
    dev_list.append(dev)
    dev.start() # thread 시작

for dev in dev_list:
    dev.join()  # wait
    print(dev.name, 'fixed', dev.fixed)