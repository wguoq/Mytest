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


def do_test(driver, url, password, config):
    pppoe_user = config.get('pppoe_user')
    pppoe_pwd = config.get('pppoe_pwd')
    Page_script.initialize(driver, url, password, username=pppoe_user, pw=pppoe_pwd)
    if Page_script.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.login(driver, admin_pw) == 1:
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
    Page_script.initialize(driver, url, password, username=pppoe_user, pw=pppoe_pwd)
    if Page_script.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.login(driver, admin_pw) == 1:
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
    with open('TestConfig.ini', 'r', encoding='utf-8') as f:
        conf = tools.get_config(f.readlines())
    for c in conf.items():
        logging.info(c)
    num = int(conf.get("reset_times"))
    test_ip = conf.get("reset_ip")
    test_url = 'http://' + test_ip
    admin_pw = conf.get("admin_pw")
    new_ssid = conf.get("new_ssid")
    old_5ssid = conf.get("default_5ssid")
    wait_time = int(conf.get("wait_time1"))
    fail = 0
    for i in range(num):
        logging.info('====run test==== %s', i+1)
        chrome = webdriver.Chrome()
        if tools.ping_ok(test_ip) == 1:
            if do_test(chrome, test_url, admin_pw, conf) == 1:
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