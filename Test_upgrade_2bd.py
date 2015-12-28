# -*- coding:utf-8 -*-

###################################
#   升级测试（降级，升级）
#   配置在testconfig.ini中
###################################
import configparser
import logging
import paramiko
from selenium import webdriver
import time
import script_page
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
    old_build = config.get('Upgrade', 'old_build')
    new_build = config.get('Upgrade', 'new_build')
    new_version = config.get('Upgrade', 'new_version')
    upgrade_wtime = int(config.get('Upgrade', 'upgrade_wtime'))
    fail = 0
    for i in range(upgrade_times):
        logging.info('===run test=== %s', i+1)
        #降级
        if script_page.open_url(driver, 'http://'+upgrade_ip) == 1:
            pass
        else:
            fail += 1
            logging.warning('===test fail===')
            logging.info("fail times ======== %s", fail)
            continue
        if script_page.login(driver, upgrade_pw) == 1:
            pass
        else:
            fail += 1
            logging.warning('===test fail===')
            logging.info("fail times ======== %s", fail)
            continue
        if script_page.upgrade(driver, old_build, upgrade_wtime) == 1:
            pass
        else:
            fail += 1
            logging.warning('===test fail===')
            logging.info("fail times ======== %s", fail)
            continue
        #升级
        if script_page.open_url(driver, 'http://'+upgrade_ip) == 1:
            pass
        else:
            fail += 1
            logging.warning('===test fail===')
            logging.info("fail times ======== %s", fail)
            continue
        if script_page.login(driver, upgrade_pw) == 1:
            pass
        else:
            fail += 1
            logging.warning('===test fail===')
            logging.info("fail times ======== %s", fail)
            continue
        if script_page.upgrade(driver, new_build, upgrade_wtime) == 1:
            pass
        else:
            fail += 1
            logging.warning('===test fail===')
            logging.info("fail times ======== %s", fail)
            continue
        #检查升级是否成功
        if script_page.open_url(driver, 'http://'+upgrade_ip) == 1:
            pass
        else:
            fail += 1
            logging.warning('===test fail===')
            logging.info("fail times ======== %s", fail)
            continue
        if script_page.login(driver, upgrade_pw) == 1:
            pass
        else:
            fail += 1
            logging.warning('===test fail===')
            logging.info("fail times ======== %s", fail)
            continue
        version = script_page.get_version(driver)
        if 'V'+new_version == version.strip():
            logging.info("test success")
        else:
            fail += 1
            logging.warning('===test fail===')
            logging.info("fail times ======== %s", fail)
            logging.info("new_version = " + new_version)
            logging.info("version = " + version)


if __name__ == '__main__':
    chrome = webdriver.Chrome()
    do_test(chrome, 'testconfig.ini')


