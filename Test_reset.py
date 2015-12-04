# -*- coding:utf-8 -*-
###################################
#   D1恢复出厂测试
#   配置在testconfig.ini中
###################################

import logging
import time
from selenium import webdriver
import Page_script
import tools

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='reset.log',
                    filemode='a')
#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


def detect_wan(driver):
    flag = ['运营商', 'DHCP']
    try:
        tip = str(driver.find_element_by_css_selector("p.tips-text").text)
        for a in flag:
            if tip.find(a) > -1:
                return a
    except Exception as e:
        print(e)
        return 0


def initialize(driver, url):
    try:
        time.sleep(3)
        driver.get(url)
        time.sleep(3)
        driver.find_element_by_id("init-protocol-checkbox").click()
        time.sleep(3)
        driver.find_element_by_id("initalize").click()
        time.sleep(30)
        wan = detect_wan(driver)
        if wan == 0:
            logging.info('wan = 跳过检测')
            driver.find_element_by_link_text(u"跳过检测").click()
        else:
            if 'DHCP' == wan:
                logging.info('wan = '+wan)
                driver.find_element_by_link_text(u"下一步").click()
                time.sleep(10)
            if '运营商' == wan:
                logging.info('wan = '+wan)
                #TODO
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


def do_test(driver, url):
    initialize(driver, url)
    if Page_script.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.login(driver, pw) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.set_5ssid(driver, new_ssid) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.reset(driver, wait_time) == 1:
        time.sleep(3)
    else:
        return 0
    initialize(driver, url)
    if Page_script.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.login(driver, pw) == 1:
        time.sleep(2)
    else:
        return 0
    ssid = Page_script.get_5ssid(driver)
    if ssid == old_5ssid:
        logging.info('test success')
        return 1
    else:
        logging.warning("===test fail===")
        logging.warning('ssid= %s', ssid)
        logging.warning('oldssid= %s', old_5ssid)
        return 0


if __name__ == '__main__':
    with open('testconfig.ini', 'r', encoding='utf-8') as f:
        conf = tools.get_config(f.readlines())
    for c in conf.items():
        logging.info(c)
    num = int(conf.get("reset_times"))
    test_ip = conf.get("reset_ip")
    test_url = 'http://' + test_ip
    pw = conf.get("admin_pw")
    new_ssid = conf.get("new_ssid")
    old_5ssid = conf.get("default_5ssid")
    wait_time = int(conf.get("wait_time1"))
    fail = 0
    for i in range(num):
        logging.info('====run test==== %s', i+1)
        chrome = webdriver.Chrome()
        if tools.ping_ok(test_ip) == 1:
            if do_test(chrome, test_url) == 1:
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