# -*- coding:utf-8 -*-
import paramiko
from selenium import webdriver
import Page_script
import re
import tools


def init(driver, url, config):
    print('D1_initialize')
    password = config.get('admin_pw')
    Page_script.open_url(driver, url)
    if Page_script.initialize(driver, url, password) == 1:
        print('init success')
    else:
        print('init fail!!!')


def login(driver, url, password):
    print('D1_login')
    Page_script.open_url(driver, url)
    if Page_script.login(driver, password) == 1:
        print('login success')
    else:
        print('login fail!!!')


def pppoe(driver, config):
    print('D1_pppoe')
    url = 'http://'+config.get('default_ip')
    password = config.get('admin_pw')
    user = conf.get('pppoe_user')
    pw = conf.get('pppoe_pwd')
    Page_script.open_url(driver, url)
    Page_script.login(driver, password)
    if Page_script.connect_pppoe(driver, user, pw) == 1:
        print('pppoe connect success')
    else:
        print('pppoe connect fail!!!')


def mac_clone(driver, url, password):
    print('D1_mac_clone')
    Page_script.open_url(driver, url)
    Page_script.login(driver, password)
    cur_mac = Page_script.clone_cur_mac(driver)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.99.1', port=22, username='root', password=password)
    stdin, stdout, stderr = ssh.exec_command('ifconfig eth0.2')
    a = tools.find_flag(stdout, 'HWaddr')
    ssh.close()
    HWaddr = str(a[0])
    if cur_mac == HWaddr[HWaddr.find('HWaddr')+len('HWaddr'):].lower().strip():
        print('mac clone success')
    else:
        print('mac clone fail!!!')


def get_case(test_list):
    a = list(filter(lambda x: re.match('^\d+\.', x), test_list))
    b = list(map(lambda x: x.strip().split('.'), a))
    c = sorted(b, key=(lambda x: x[0]))
    return c


def ck_format(test_case):
    for i in test_case:
        if len(i) != 2:
            print('格式错误: ', '.'.join(i))
            return 0
    return 1


def ck_oder(test_case):
    i = len(test_case) - 1
    while i >= 0:
        a = test_case[i]
        b = test_case[:i]
        for c in b:
            if a[0] == c[0]:
                print('序号重复：', '.'.join(a), '  ', '.'.join(c))
                return 0
        i -= 1
    return 1


if __name__ == '__main__':
    with open('testconfig.ini', 'r', encoding='utf-8') as f:
        conf = tools.get_config(f.readlines())
    with open('Testlist.ini', 'r', encoding='utf-8') as f:
        test_lst = f.readlines()
    chrome = webdriver.Chrome()
    admin_pw = conf.get('admin_pw')
    default_url = 'http://'+conf.get('default_ip')

    #{testname:(func,[params])} testname必须和配置文件里面一样
    script = {'D1_initialize': (init, [chrome, default_url, conf]),
              'D1_login': (login, [chrome, default_url, admin_pw]),
              'D1_pppoe': (pppoe, [chrome, conf])}

    ts_case = get_case(test_lst)
    if ck_format(ts_case) & ck_oder(ts_case) == 1:
        build = []
        for t in ts_case:
            if t[1] in script:
                build.append(script.get(t[1]))
        for func, param in build:
            func(*param)
        chrome.close()
    else:
        print('22222')



