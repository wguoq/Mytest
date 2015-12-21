# -*- coding: utf-8 -*-
###################################
#   拨号测试
#   配置在testconfig.ini中
###################################

import logging
from selenium import webdriver
import time
import Page_script
import tools

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='pppoe.log',
                    filemode='a')
#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


def do_test(driver, url):
    if Page_script.open_url(driver, url):
        time.sleep(3)
    else:
        return 0
    if Page_script.login(driver, pw):
        time.sleep(3)
    else:
        return 0
    if Page_script.connect_pppoe(driver, pppoe_pst, pppoe_pwd) == 1:
        time.sleep(3)
        return 1
    else:
        return 0


if __name__ == '__main__':
    with open('TestConfig.ini', 'r', encoding='utf-8') as f:
        conf = tools.get_config(f.readlines())
    for c in conf.items():
        logging.info(c)
    num = int(conf.get("pppoe_times"))
    test_ip = conf.get("pppoe_ip")
    test_url = 'http://'+test_ip
    pw = conf.get("admin_pw")
    pppoe_pst = conf.get("pppoe_user")
    pppoe_pwd = conf.get("pppoe_pwd")
    chrome = webdriver.Chrome()
    for i in range(num):
        logging.info('====run test==== %s', i)
        if do_test(chrome, test_url) == 1:
            logging.info("connect success")
            time.sleep(3)
        else:
            logging.warning("connect fail")
    chrome.quit()
