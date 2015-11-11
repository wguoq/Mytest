# -*- coding:utf-8 -*-
###################
#   刷网页挂机测试
###################

import threading
import time
from selenium import webdriver
import tools2


def testurl(url_lst):
    o = 1
    while o > 0:
        driver = webdriver.Chrome()
        for l in url_lst:
            try:
                driver.get(l)
                time.sleep(30)
            except Exception as e:
                print(e)
                time.sleep(30)
        driver.quit()


def logtime():
    f = open(logfile)
    while 2 > 1:
        date = time.ctime(time.time())
        lock.acquire()
        f.write(date+"\n")
        f.flush()
        lock.release()
        print(date)
        time.sleep(3600)
    f.close()

op = open("10url", "r")
url_list = op.readlines()
op.close()
ip = "192.168.99.1"
lock = threading.RLock()
logfile = "10url.log"
port = "COM3"
c1 = threading.Thread(target=logtime)
c2 = threading.Thread(target=tools2.get_serial_log, args=(port, logfile, lock))
threads = [c1, c2]
for i in range(5):
    ti = threading.Thread(target=testurl, args=(url_list,))
    threads.append(ti)
for t in threads:
    t.start()