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
        for i in url_lst:
            try:
                driver.get(i)
                time.sleep(5)
            except Exception as e:
                print(e)
                time.sleep(5)
        driver.quit()


def tudou():
    diver = webdriver.Chrome()
    o = 1
    while o > 0:
        try:
            diver.refresh()
            time.sleep(1)
            diver.get("http://www.tudou.com/albumplay/_93DHcFhgf4/J7OVDM8p02Q.html")
            time.sleep(10800)
        except Exception as e:
            print(e)


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
t1 = threading.Thread(target=testurl, args=(url_list,))
t2 = threading.Thread(target=testurl, args=(url_list,))
t3 = threading.Thread(target=testurl, args=(url_list,))
t4 = threading.Thread(target=testurl, args=(url_list,))
t9 = threading.Thread(target=tudou)
t10 = threading.Thread(target=logtime)
t11 = threading.Thread(target=tools2.get_serial_log, args=(port, logfile, lock))
threads = [t1, t2, t3, t4, t9, t10, t11]
for t in threads:
    time.sleep(1)
    t.start()
