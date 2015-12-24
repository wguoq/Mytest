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
    restart_times = int(config.get('Restart', 'restart_times'))
    restart_ip = config.get('Restart', 'restart_ip')
    restart_pw = config.get('Restart', 'restart_pw')
    restart_wtime = int(config.get('Restart', 'restart_wtime'))
    for i in range(restart_times):
        logging.info('===run test=== %s', i+1)
        fail = 0
        if Page_script.open_url(driver, 'http://'+restart_ip) == 1:
            pass
        else:
            continue
        if Page_script.login(driver, restart_pw) == 1:
            pass
        else:
            continue
        if Page_script.restart(driver, restart_wtime) == 1:
            pass
        else:
            continue
        if Page_script.open_url(driver, 'http://'+restart_ip) == 1:
            pass
        else:
            continue
        if Page_script.login(driver, restart_pw) == 1:
            try:
                print('request baidu')
                urllib.request.urlretrieve('https://www.baidu.com')
                time.sleep(1)
                print('request qq')
                urllib.request.urlretrieve('http://www.qq.com/')
                time.sleep(1)
                logging.info('test success')
            except Exception as e:
                fail += 1
                logging.info('===test fail===')
                logging.info("fail times ======== %s", fail)
        else:
            fail += 1
            logging.info('===test fail===')
            logging.info("fail times ======== %s", fail)
    driver.quit()


if __name__ == '__main__':
    chrome = webdriver.Chrome()
    do_test(chrome, 'testconfig.ini')


