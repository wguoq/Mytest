# -*- coding:utf-8 -*-
import logging
import paramiko
from selenium import webdriver
import time
import XcloudScript
import tools2
import threading
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
    if XcloudScript.open_url(driver, url) == 1:
        time.sleep(3)
    else:
        return 0
    if XcloudScript.login(driver, pw) == 1:
        time.sleep(3)
    else:
        return 0
    logging.info("version = %s", XcloudScript.get_version(driver))
    if XcloudScript.upgrade(driver, new_build, wait) == 1:
        time.sleep(3)
    else:
        return 0
    #检查升级是否成功
    if tools2.ping_ok(test_ip):
        try:
            ssh.connect(test_ip, 22, "root", pw)
            this_version = tools2.uci_cmd(ssh, uci_sys, ver_flag)
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


def get_test_result(testlog):
    fail = 0
    f = open(testlog, "a")
    for i in range(num):
        x = "====run test==== " + str(i+1)
        logging.info(x)
        lock.acquire()
        f.write(x + "\n")
        f.flush()
        lock.release()
        if tools2.ping_ok(test_ip) == 1:
            time.sleep(5)
            chrome = webdriver.Chrome()
            if dotest(chrome, test_url) == 1:
                time.sleep(1)
                chrome.quit()
            else:
                chrome.quit()
                fail += 1
                a = " =======test fail======== " + str(fail)
                time.sleep(1)
                lock.acquire()
                f.write(a + "\n")
                f.flush()
                lock.release()
        else:
            fail += 1
            a = " =======ping fail======== " + str(fail)
            time.sleep(1)
            lock.acquire()
            f.write(a + "\n")
            f.flush()
            lock.release()
            time.sleep(10)
    f.close()

op = open('testconfig.ini', 'r')
conf = tools2.getconfig(op)
op.close()
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
port = "COM3"
logfile = "123.log"
lock = threading.RLock()
t1 = threading.Thread(target=tools2.get_serial_log, args=(port, logfile, lock))
t2 = threading.Thread(target=get_test_result, args=(logfile,))

threads = [t1, t2]

for t in threads:
    time.sleep(1)
    t.start()