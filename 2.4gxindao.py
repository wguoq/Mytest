# -*- coding:utf-8 -*-
#######################
#   D1切换信道测试
#######################

import logging
import threading
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
import XcloudScript
import tools2

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='reset.log',
                    filemode='w')
#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


def channel(i):
    try:
        XcloudScript.open_url(driver, test_url)
        time.sleep(3)
        XcloudScript.login(driver, pw)
        time.sleep(3)
        driver.find_element_by_id("wifinfo_24").click()
        time.sleep(5)
        Select(driver.find_element_by_id("wifi_channel")).select_by_value(i)
        time.sleep(3)
        driver.find_element_by_css_selector("a.subbtn.saveStatus > b").click()
        time.sleep(3)
        return True
    except Exception as e:
        print(e)
        return False


def dotest():
    ts = 1
    o = 0
    while o < 5:
        for i in range(14):
            if i == 0:
                continue
            i = str(i)
            a = "channel=="+i
            b = "times=="+str(ts)
            lock.acquire()
            f = open("xindao.log", "a")
            f.write(a + "\n")
            f.write(b + "\n")
            f.close()
            lock.release()
            if channel(i):
                o = 0
                ts += 1
                time.sleep(40)
            else:
                o += 1
                ts += 1



def get_time():
    a = 123
    while a > 0:
        s = time.ctime(time.time())
        lock.acquire()
        f = open("xindao.log", "a")
        f.write(s + "\n")
        f.close()
        lock.release()
        time.sleep(300)



if __name__ == '__main__':
    conf = tools2.getconfig(open('testconfig.ini', 'r'))
    test_ip = conf.get("reset_ip")
    test_url = 'http://'+test_ip
    pw = conf.get("pw")
    driver = webdriver.Chrome()
    com = "COM3"
    serlog = "xindao.log"
    lock = threading.RLock()
    t1 = threading.Thread(target=tools2.get_serial_log, args=(com, serlog, lock))
    t2 = threading.Thread(target=dotest)
    t3 = threading.Thread(target=get_time)
    threads = [t1, t2]
    for t in threads:
        time.sleep(1)
        t.start()

