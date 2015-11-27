# -*- coding:utf-8 -*-
#######################
#   D1切换信道测试
#   配置在testconfig.ini中
#######################

import logging
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
import Page_script
import tools

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='2.4xindao.log',
                    filemode='a')
#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


def channel(driver, i):
    try:
        driver.find_element_by_id("wifinfo_24").click()
        time.sleep(5)
        Select(driver.find_element_by_id("wifi_channel")).select_by_value(i)
        time.sleep(3)
        driver.find_element_by_css_selector("a.subbtn.saveStatus > b").click()
        time.sleep(3)
        return 1
    except Exception as e:
        print(e)
        return 0


def do_test(driver, url):
    Page_script.open_url(driver, url)
    time.sleep(3)
    Page_script.login(driver, pw)
    time.sleep(3)
    times = 1
    o = 0
    while o < 3:
        for i in range(13):
            i = str(i+1)
            logging.info(times)
            if channel(driver, i) == 1:
                o = 0
                times += 1
                time.sleep(60)
            else:
                o += 1
                times += 1
                time.sleep(60)

if __name__ == "__main__":
    with open('testconfig.ini', 'r', encoding='utf-8') as f:
        conf = tools.get_config(f)
    for c in conf.items():
        logging.info(c)
    test_url = 'http://'+conf.get("default_ip")
    pw = conf.get("admin_pw")
    chrome = webdriver.Chrome()
    do_test(chrome, test_url)
