# -*- coding:utf-8 -*-

###################################
#   升级测试（同一个版本升级）
#   打开SSH
#   配置在testconfig.ini中
###################################
import configparser
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


def do_test(driver, config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='UTF-8')
    upgrade_times = int(config.get('Upgrade', 'upgrade_times'))
    upgrade_ip = config.get('Upgrade', 'upgrade_ip')
    upgrade_pw = config.get('Upgrade', 'upgrade_pw')
    new_build = config.get('Upgrade', 'new_build')
    new_version = config.get('Upgrade', 'new_version')
    upgrade_wtime = int(config.get('Upgrade', 'upgrade_wtime'))
    for i in range(upgrade_times):
        logging.info('===run test=== %s', i+1)
        if Page_script.open_url(driver, 'http://'+upgrade_ip) == 1:
            pass
        else:
            continue
        if Page_script.login(driver, upgrade_pw) == 1:
            pass
        else:
            continue
        if Page_script.upgrade(driver, new_build, upgrade_wtime) == 1:
            pass
        else:
            continue
        #检查升级是否成功
        if Page_script.open_url(driver, 'http://'+upgrade_ip) == 1:
            pass
        else:
            continue
        if Page_script.login(driver, upgrade_pw) == 1:
            pass
        else:
            continue
        if new_version == this_version.strip():
            logging.info("test success")

        else:
            logging.info("new_version = " + new_version)
            logging.info("this_version = " + this_version)





if __name__ == '__main__':
    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    version = '0.0.0.1'
    cmd1 = 'sed -i "s/DISTRIB_RELEASE=.*/DISTRIB_RELEASE=\\"'
    cmd2 = '\\"/g" /etc/openwrt_release'
    cmd = cmd1+version+cmd2
    uci_sys = 'uci show system'
    ver_flag = 'system.@system[0].ver'
    '''
    fail = 0
    for i in range(num):
        logging.info('====run test==== %s', i+1)
        chrome = webdriver.Chrome()
        if tools.ping_ok(test_ip):
            if do_test(chrome, test_url) == 1:
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

