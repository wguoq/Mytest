# -*- coding:utf-8 -*-
#########################
#   潘多拉切换信道测试
#########################

import logging
from selenium import webdriver
import time
from selenium.webdriver.support.select import Select

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='restart.log',
                    filemode='w')
#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


def channel(value):
    try:
        driver.get("http://192.168.1.1/cgi-bin/luci/;stok=7d83d79774091e66d8f2e8373d39ce8c/admin/network/wireless/ra0.network1/")
        time.sleep(3)
        driver.find_element_by_id("focus_password").clear()
        driver.find_element_by_id("focus_password").send_keys("admin")
        driver.find_element_by_css_selector("input.cbi-button.cbi-button-apply").click()
        time.sleep(5)
        Select(driver.find_element_by_id("cbid.wireless.ra0._mode_freq.channel")).select_by_value(value)
        driver.find_element_by_name("cbi.apply").click()
        time.sleep(10)
    except Exception as e:
        logging.warning('2.4G channel Fail %s' % e)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    o = 0
    while o == 0:
        for i in range(14):
            if i == 0:
                continue
            i = str(i)
            logging.info("i = %s", i)
            channel(i)




