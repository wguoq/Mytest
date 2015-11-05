# -*- coding:utf-8 -*-

###################################
#   D1恢复出厂测试
#   测试时拔掉wan口网线
#   在testconfig.ini中修改配置项:
#   resetnum=测试次数
#   reset_ip=路由器内网ip
#   pw=登录密码
#   old_5ssid=默认5gssid
#   wait_time1=恢复出厂等待时间
###################################

import logging
import time
from selenium import webdriver
import XcloudScript
import tools

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
    if XcloudScript.open_url(driver, test_url) == 1:
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
    if XcloudScript.open_url(driver, test_url) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.login(driver, pw) == 1:
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

if __name__ == '__main__':
    op = open('testconfig.ini', 'r')
    conf = tools.getconfig(op)
    op.close()
    logging.info(conf)
    num = int(conf.get("resetnum"))
    test_ip = conf.get("reset_ip")
    test_url = 'http://'+test_ip
    pw = conf.get("pw")
    new_ssid = conf.get("new_ssid")
    old_5ssid = conf.get("old_5ssid")
    wait_time = int(conf.get("wait_time1"))
    fail = 0
    for i in range(num):
        logging.info('====run test==== %s', i+1)
        chrome = webdriver.Chrome()
        if tools.ping_ok(test_ip) == 1:
            if dotest(chrome, test_url) == 1:
                chrome.quit()
            else:
                fail += 1
                logging.info("fail times ======== %s", fail)
                chrome.quit()
        else:
            logging.info("===ping fail===")
            fail += 1
            logging.info("fail times ======== %s", fail)
            chrome.quit()
            time.sleep(10)