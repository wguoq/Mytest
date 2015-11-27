# -*- coding: utf-8 -*-
###################################
#   拨号测试
#   在testconfig.ini中修改配置项:
#   pppoenum=测试次数
#   pppoe_ip=路由器内网ip
#   pw=登录密码
#   pppoe_pst2=拨号账号
#   pppoe_pwd=拨号密码
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


def dotest(driver, url):
    if Page_script.open_url(driver, url):
        time.sleep(3)
    else:
        return 0
    if Page_script.login(driver, pw):
        time.sleep(3)
    else:
        return 0
    if Page_script.connect_pppoe(driver, pppoe_pst, pppoe_pwd):
        time.sleep(3)
        if "断开" == driver.find_element_by_xpath("//span[@id='pppoe_btn']/a/b").text:
            Page_script.disconnect_pppoe(driver)
            return 1
        else:
            Page_script.disconnect_pppoe(driver)
            return 0
    else:
        Page_script.disconnect_pppoe(driver)
        return 0


if __name__ == '__main__':
    op = open('testconfig.ini', 'r')
    conf = tools.getconfig(op)
    op.close()
    logging.info(conf)
    num = int(conf.get("pppoenum"))
    test_ip = conf.get("pppoe_ip")
    test_url = 'http://'+test_ip
    pw = conf.get("pw")
    pppoe_pst = conf.get("pppoe_pst2")
    pppoe_pwd = conf.get("pppoe_pwd")
    chrome = webdriver.Chrome()
    for i in range(num):
        logging.info('====run test==== %s', i)
        if dotest(chrome, test_url):
            logging.info("connect success")
            time.sleep(3)
        else:
            logging.warning("connect fail")
    chrome.quit()
