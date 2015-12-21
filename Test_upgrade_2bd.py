# -*- coding:utf-8 -*-

###################################
#   升级测试(降级/升级)
#   配置在testconfig.ini中
###################################

import logging
import paramiko
from selenium import webdriver
import time
import Page_script
import tools
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='UpgradeTest.log',
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
    #降级
    if Page_script.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.login(driver, pw) == 1:
        time.sleep(3)
        logging.info("version = %s", Page_script.get_version(driver))
    else:
        return 0
    if Page_script.upgrade(driver, old_build, wait) == 1:
        time.sleep(3)
    else:
        return 0
    #升级
    if Page_script.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if Page_script.login(driver, pw) == 1:
        time.sleep(3)
        logging.info("version = %s", Page_script.get_version(driver))
    else:
        return 0
    if Page_script.upgrade(driver, new_build, wait) == 1:
        time.sleep(3)
    else:
        return 0
    #检查升级是否成功
    if tools.ping_ok(test_ip):
        try:
            ssh.connect(test_ip, 22, "root", pw)
            this_version = tools.uci_cmd(ssh, uci_sys, ver_flag)
            if new_version == this_version.strip():
                logging.info("test success")
                return 1
            else:
                logging.info("new_version = " + new_version)
                logging.info("this_version = " + this_version)
                return 0
        except Exception as e:
            logging.warning(e)
            return 0
    else:
        return 0


if __name__ == '__main__':
    with open('TestConfig.ini', 'r', encoding='utf-8') as f:
        conf = tools.get_config(f.readlines())
    for c in conf.items():
        logging.info(c)
    num = int(conf.get("upgrade_times"))
    test_ip = conf.get("upgrade_ip")
    test_url = 'http://'+test_ip
    pw = conf.get("admin_pw")
    old_build = conf.get("old_build")
    new_build = conf.get("new_build")
    new_version = conf.get("new_version")
    wait = int(conf.get("wait_time2"))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    uci_sys = 'uci show system'
    ver_flag = 'system.@system[0].ver'
    fail = 0
    for i in range(num):
        logging.info('====run test==== %s', i+1)
        chrome = webdriver.Chrome()
        if tools.ping_ok(test_ip) == 1:
            if dotest(chrome, test_url) == 1:
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