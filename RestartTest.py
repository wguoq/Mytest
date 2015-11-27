# -*- coding:utf-8 -*-

###################################
#   重启测试
#   在testconfig.ini中修改配置项:
#   restartnum=测试次数
#   restart_ip=路由器内网ip
#   pw=登录密码
#   wait_time1=重启等待时间
###################################

import logging
from selenium import webdriver
import time
import XcloudScript
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


def dotest(driver, url):
    if XcloudScript.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.login(driver, pw) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.restart(driver, wait_time) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.login(driver, pw) == 1:
        return 1
    else:
        return 0


if __name__ == '__main__':
    op = open('testconfig.ini', 'r')
    conf = tools.getconfig(op)
    op.close()
    logging.info(conf)
    num = int(conf.get("restartnum"))
    test_ip = conf.get("restart_ip")
    test_url = 'http://'+test_ip
    pw = conf.get("pw")
    wait_time = int(conf.get("wait_time1"))
    fail = 0
    baidu = 'https://www.baidu.com'
    qq = 'http://www.qq.com/'
    for i in range(num):
        logging.info('====run test==== %s', i+1)
        chrome = webdriver.Chrome()
        if dotest(chrome, test_url) == 1:
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

