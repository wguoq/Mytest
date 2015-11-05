# -*- coding:utf-8 -*-
import logging
import threading
from selenium import webdriver
import time
import serial
import XcloudScript
import tools2

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='restart.log',
                    filemode='w')
#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


def dotest(driver, url):
    if XcloudScript.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.login(driver, pw) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.restart(driver, wait_time) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.login(driver, pw) == 1:
        logging.info('test success')
        return 1
    else:
        logging.warning('===test fail===')
        return 0


def get_test_result(testlog):
    fail = 0
    f = open(testlog, "a")
    for i in range(num):
        x = "====run test==== " + str(i+1)
        logging.info(x)
        lock.acquire()
        f.write(x + "\n")
        f.flush()
        lock.release()
        if tools2.ping_ok(test_ip) == 1:
            time.sleep(5)
            chrome = webdriver.Chrome()
            if dotest(chrome, test_url) == 1:
                time.sleep(1)
                chrome.quit()
            else:
                chrome.quit()
                fail += 1
                a = " =======test fail======== " + str(fail)
                time.sleep(1)
                lock.acquire()
                f.write(a + "\n")
                f.flush()
                lock.release()
        else:
            fail += 1
            a = " =======ping fail======== " + str(fail)
            time.sleep(1)
            lock.acquire()
            f.write(a + "\n")
            f.flush()
            lock.release()
            time.sleep(10)
    f.close()


op = open('testconfig.ini', 'r')
conf = tools2.getconfig(op)
op.close()
logging.info(conf)
num = int(conf.get("restartnum"))
test_ip = conf.get("restart_ip")
test_url = 'http://' + test_ip
pw = conf.get("pw")
wait_time = int(conf.get("wait_time1"))
port = "COM3"
file = "123.log"
lock = threading.RLock()
t1 = threading.Thread(target=tools2.get_serial_log, args=(port, file, lock,))
t2 = threading.Thread(target=get_test_result, args=(file,))
threads = [t1, t2]
for t in threads:
    t.start()