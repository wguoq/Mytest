# -*- coding:utf-8 -*-

###################################
#   升级测试(降级升级一起)
#   打开SSH
#   在testconfig.ini中修改配置项:
#   updatanum=测试次数
#   upgrade_ip=路由器内网ip
#   pw=登录密码
#   new_build=新固件文件地址
#   new_version=新固件版本
#   old_build=旧固件文件地址
#   old_version=旧固件版本
#   wait_time2=升级等待时间
###################################

import logging
import paramiko
from selenium import webdriver
import time
import XcloudScript
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
    if XcloudScript.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.login(driver, pw) == 1:
        time.sleep(3)
        logging.info("version = %s", XcloudScript.get_version(driver))
    else:
        return 0
    if XcloudScript.upgrade(driver, old_build, wait) == 1:
        time.sleep(3)
    else:
        return 0
    #升级
    if XcloudScript.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.login(driver, pw) == 1:
        time.sleep(3)
        logging.info("version = %s", XcloudScript.get_version(driver))
    else:
        return 0
    if XcloudScript.upgrade(driver, new_build, wait) == 1:
        time.sleep(3)
    else:
        return 0
    #检查升级是否成功
    if tools.ping_ok(test_ip):
        try:
            ssh.connect(test_ip, 22, "root", pw)
            this_version = tools.uci_cmd(ssh, uci_sys, ver_flag)
            if new_version == this_version:
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
    op = open('testconfig.ini', 'r')
    conf = tools.getconfig(op)
    op.close()
    logging.info(conf)
    num = int(conf.get("updatanum"))
    test_ip = conf.get("upgrade_ip")
    test_url = 'http://'+test_ip
    pw = conf.get("pw")
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