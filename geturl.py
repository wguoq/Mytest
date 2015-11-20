# -*- coding:utf-8 -*-
###################
#   刷网页挂机测试
###################
import threading
import time
from selenium import webdriver


def openweb(urlist, delay):
    while True:
        driver = webdriver.Chrome()
        for l in urlist:
            try:
                l = l.strip()
                driver.get(l)
                time.sleep(delay)
            except Exception as e:
                print(e)
                time.sleep(delay)
        driver.quit()


op = open("URLlist", "r")
url_lst = op.readlines()
op.close()
for i in range(5):
    ti = threading.Thread(target=openweb, args=(url_lst, 120,))
    time.sleep(10)
    ti.start()