# -*- coding:utf-8 -*-
###################
#   刷网页挂机测试
###################

import threading
import time
from selenium import webdriver
import tools2
exitFlag = 0


def testurl(url):
    o = 1
    while o > 0:
        driver = webdriver.Chrome()
        for i in url:
            try:
                N = time.time()
                driver.get(i)
                M = time.time()
                print(M - N)
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
            time.sleep(7200)
            diver.get("http://www.baidu.com")
            time.sleep(5)
        except Exception as e:
            print(e)


def logtime():
    o = 1
    while o > 0:
        t = time.ctime(time.time())
        lock.acquire()
        f = open("10url.log", "a")
        f.write(t+"\n")
        f.close()
        lock.release()
        print(t)
        time.sleep(1800)





url_list = open("10url", "r").readlines()
ip = "192.168.99.1"
lock = threading.RLock()
logfile = "10url.log"
port = "COM3"
t1 = threading.Thread(target=testurl, args=(url_list,))
t2 = threading.Thread(target=testurl, args=(url_list,))
t3 = threading.Thread(target=testurl, args=(url_list,))
t4 = threading.Thread(target=testurl, args=(url_list,))
t5 = threading.Thread(target=testurl, args=(url_list,))
t9 = threading.Thread(target=tudou)
t10 = threading.Thread(target=logtime)
t11 = threading.Thread(target=tools2.get_serial_log, args=(port, logfile, lock))

threads = [t1, t2, t3, t4, t5]
t1.start()
'''
for t in threads:
    time.sleep(1)
    t.start()
'''