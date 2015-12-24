# -*- coding:utf-8 -*-

###################################
#   重启测试
#   配置在testconfig.ini中
###################################
import configparser
import logging
from selenium import webdriver
import time
import Page_script
import tools
import urllib.request

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='restart.log',
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
    restart_times = config.get('Restart', 'restart_times')
    default_ip = config.get('Reset', 'default_ip')
    default_pw = config.get('Reset', 'default_pw')
    new_ssid = config.get('Reset', 'new_ssid')
    default_5ssid = config.get('Reset', 'default_5ssid')
    pppoe_user = config.get('PPPOE', 'pppoe_user')
    pppoe_pwd = config.get('PPPOE', 'pppoe_pwd')
    reset_wtime = config.get('Reset', 'reset_wtime')


    if Page_script.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.login(driver, pw) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.restart(driver, wait_time) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.login(driver, pw) == 1:
        return 1
    else:
        return 0


if __name__ == '__main__':
    with open('testconfig.ini', 'r', encoding='utf-8') as f:
        conf = tools.get_config(f.readlines())
    for c in conf.items():
        logging.info(c)
    num = int(conf.get("restart_times"))
    test_ip = conf.get("restart_ip")
    test_url = 'http://'+test_ip
    pw = conf.get("admin_pw")
    wait_time = int(conf.get("wait_time1"))
    fail = 0
    baidu = 'https://www.baidu.com'
    qq = 'http://www.qq.com/'
    for i in range(num):
        logging.info('====run test==== %s', i+1)
        chrome = webdriver.Chrome()
        if do_test(chrome, test_url) == 1:
            chrome.quit()
            try:
                print('request baidu')
                urllib.request.urlretrieve(baidu)
                time.sleep(1)
                print('request qq')
                urllib.request.urlretrieve(qq)
                time.sleep(1)
                logging.info('test success')
            except Exception as e:
                logging.warning(e)
                logging.warning('====request '+baidu+' fail====')
                fail += 1
                logging.info("fail times ======== %s", fail)
                time.sleep(1)
        else:
            fail += 1
            logging.info('====test fail====')
            logging.info("fail times ======== %s", fail)
            chrome.quit()

