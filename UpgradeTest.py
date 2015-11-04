# -*- coding:utf-8 -*-

###################################
#   升级测试（同一个版本升级）
#   打开SSH
#   在testconfig.ini中修改配置项:
#   updatanum=测试次数
#   upgrade_ip=路由器内网ip
#   pw=登录密码
#   new_build=新固件文件地址
#   new_version=新固件版本
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
                    filemode='w')
#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


def dotest(driver, url):
    try:
        ssh.connect(test_ip, 22, "root", pw)
        ssh.exec_command(cmd)
    except Exception as e:
        logging.warning(e)
        return 0
    if XcloudScript.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.login(driver, pw) == 1:
        time.sleep(3)
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
    conf = tools.getconfig(open('testconfig.ini', 'r'))
    logging.info(conf)
    num = int(conf.get("updatanum"))
    test_ip = conf.get("upgrade_ip")
    test_url = 'http://'+test_ip
    pw = conf.get("pw")
    new_build = conf.get("new_build")
    new_version = conf.get("new_version")
    wait = int(conf.get("wait_time2"))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    version = '0.0.0.1'
    cmd1 = 'sed -i "s/DISTRIB_RELEASE=.*/DISTRIB_RELEASE=\\"'
    cmd2 = '\\"/g" /etc/openwrt_release'
    cmd = cmd1+version+cmd2
    uci_sys = 'uci show system'
    ver_flag = 'system.@system[0].ver'
    fail = 0
    for i in range(num):
        logging.info('====run test==== %s', i+1)
        chrome = webdriver.Chrome()
        if tools.ping_ok(test_ip):
            if dotest(chrome, test_url) == 1:
                chrome.quit()
            else:
                fail += 1
                logging.info("fail times ======== %s", fail)
                chrome.quit()
        else:
            logging.info("===ping host fail===")
            fail += 1
            logging.info("fail times ======== %s", fail)
            chrome.quit()
            time.sleep(10)