# -*- coding: utf-8 -*-
###################################
#   拨号测试
#   配置在testconfig.ini中
###################################
import configparser
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


def do_test(driver, config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='UTF-8')
    pppoe_times = config.get('PPPOE', 'pppoe_times')
    pppoe_user = config.get('PPPOE', 'pppoe_user')
    pppoe_pwd = config.get('PPPOE', 'pppoe_pwd')
    url = 'http://'+config.get('PPPOE', 'pppoe_ip')
    pppoe_pw = config.get('PPPOE', 'pppoe_pw')
    fail = 0
    if Page_script.open_url(driver, url):
        time.sleep(3)
    else:
        return 0
    if Page_script.login(driver, pppoe_pw):
        time.sleep(3)
    else:
        return 0
    for i in range(int(pppoe_times)):
        logging.info('===run test=== %s', i+1)
        if Page_script.connect_pppoe(driver, pppoe_user, pppoe_pwd) == 1:
            time.sleep(3)
            logging.info("connect success")
        else:
            fail += 1
            logging.warning("===connect fail===")
            logging.info("fail times ======== %s", fail)


if __name__ == '__main__':
    chrome = webdriver.Chrome()
    do_test(chrome, 'testconfig.ini')
    chrome.quit()
