# -*- coding:utf-8 -*-
###################################
#   D1恢复出厂测试
#   配置在testconfig.ini中
###################################
import configparser
import logging
from selenium import webdriver
import script_page

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


def do_test(driver, config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='UTF-8')
    reset_times = int(config.get('Reset', 'reset_times'))
    default_ip = config.get('Default', 'default_ip')
    default_pw = config.get('Default', 'default_pw')
    new_ssid = config.get('Reset', 'new_ssid')
    default_5ssid = config.get('Reset', 'default_5ssid')
    pppoe_user = config.get('PPPOE', 'pppoe_user')
    pppoe_pwd = config.get('PPPOE', 'pppoe_pwd')
    reset_wtime = int(config.get('Reset', 'reset_wtime'))
    for i in range(reset_times):
        logging.info('===run test=== %s', i+1)
        fail = 0
        script_page.initialize(driver, 'http://' + default_ip, default_pw, pppoe_user, pppoe_pwd)
        if script_page.open_url(driver, 'http://'+default_ip) == 1:
            pass
        else:
            fail += 1
            logging.warning("===test fail===")
            logging.info("fail times ======== %s", fail)
            continue
        if script_page.login(driver, default_pw) == 1:
            pass
        else:
            fail += 1
            logging.warning("===test fail===")
            logging.info("fail times ======== %s", fail)
            continue
        if script_page.set_5ssid(driver, new_ssid) == 1:
            pass
        else:
            fail += 1
            logging.warning("===test fail===")
            logging.info("fail times ======== %s", fail)
            continue
        if script_page.reset(driver, reset_wtime) == 1:
            pass
        else:
            fail += 1
            logging.warning("===test fail===")
            logging.info("fail times ======== %s", fail)
            continue
        script_page.initialize(driver, 'http://' + default_ip, default_pw, username=pppoe_user, pw=pppoe_pwd)
        if script_page.open_url(driver, 'http://'+default_ip) == 1:
            pass
        else:
            fail += 1
            logging.warning("===test fail===")
            logging.info("fail times ======== %s", fail)
            continue
        if script_page.login(driver, default_pw) == 1:
            pass
        else:
            fail += 1
            logging.warning("===test fail===")
            logging.info("fail times ======== %s", fail)
            continue
        ssid5 = script_page.get_5ssid(driver)
        if ssid5 == default_5ssid:
            logging.info('test success')
        else:
            fail += 1
            logging.warning("===test fail===")
            logging.info("fail times ======== %s", fail)
            logging.warning('5Gssid= %s', ssid5)
            logging.warning('default_5ssid= %s', default_5ssid)
            continue

if __name__ == '__main__':
    chrome = webdriver.Chrome()
    do_test(chrome, 'testconfig.ini')