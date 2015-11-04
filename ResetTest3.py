# -*- coding:utf-8 -*-
import logging
import threading
import time
from selenium import webdriver
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


def initialize(driver, url):
    try:
        time.sleep(3)
        driver.get(url)
        time.sleep(3)
        driver.find_element_by_id("init-protocol-checkbox").click()
        time.sleep(3)
        driver.find_element_by_id("initalize").click()
        time.sleep(5)
        driver.find_element_by_link_text(u"跳过检测").click()
        time.sleep(3)
        driver.find_element_by_id("key").clear()
        time.sleep(3)
        driver.find_element_by_id("key").send_keys("12345678")
        time.sleep(3)
        driver.find_element_by_id("wifi").click()
        time.sleep(10)
        driver.find_element_by_link_text(u"登录路由器").click()
        time.sleep(5)
        return 1
    except Exception as e:
        print(e)
        return 0


def dotest(driver, url):
    initialize(driver, url)
    if XcloudScript.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.login(driver, pw) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.set_5ssid(driver, new_ssid) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.reset(driver, wait_time) == 1:
        time.sleep(3)
    else:
        return 0
    initialize(driver, test_url)
    if XcloudScript.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.login(driver, pw):
        time.sleep(2)
    else:
        return 0
    ssid = XcloudScript.get_5ssid(driver)
    if ssid == old_5ssid:
        logging.info('test success')
        return 1
    else:
        logging.warning("===test fail===")
        logging.warning('ssid= %s', ssid)
        logging.warning('oldssid= %s', old_5ssid)
        return 0


def get_test_result(testlog):
    fail = 0
    for i in range(num):
        x = "====run test==== " + str(i+1)
        logging.info(x)
        lock.acquire()
        f = open(testlog, "a")
        f.write(x + "\n")
        f.close()
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
                f = open(testlog, "a")
                f.write(a + "\n")
                f.close()
                lock.release()
        else:
            fail += 1
            a = " =======ping fail======== " + str(fail)
            time.sleep(1)
            lock.acquire()
            f = open(testlog, "a")
            f.write(a + "\n")
            f.close()
            lock.release()
            time.sleep(10)


conf = tools2.getconfig(open('testconfig.ini', 'r'))
logging.info(conf)
new_ssid = conf.get("new_ssid")
old_5ssid = conf.get("old_5ssid")
num = int(conf.get("resetnum"))
test_ip = conf.get("reset_ip")
test_url = 'http://' + test_ip
pw = conf.get("pw")
wait_time = int(conf.get("wait_time1"))
port = "COM3"
file = "123.log"
lock = threading.RLock()
t1 = threading.Thread(target=get_test_result, args=(file,))
t2 = threading.Thread(target=tools2.get_serial_log, args=(port, file, lock))

threads = [t1, t2]

for t in threads:
    time.sleep(1)
    t.start()
