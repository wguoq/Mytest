# -*- coding:utf-8 -*-
from selenium import webdriver
import Page_script
import re
import tools


def initialize(driver, config):
    print('D1_initialize')
    url = 'http://'+config.get('default_ip')
    password = config.get('admin_pw')
    Page_script.initialize(driver, url, password)


def login(driver, config):
    print('D1_login')
    url = 'http://'+config.get('default_ip')
    password = config.get('admin_pw')
    Page_script.open_url(driver, url)
    Page_script.login(driver, password)


def pppoe(driver, config):
    print('D1_pppoe')


D1 = {'D1_initialize': initialize,
      'D1_login': login,
      'D1_pppoe': pppoe}


def get_case(test_list):
    a = list(filter(lambda x: re.match('^\d+\.', x), test_list))
    b = list(map(lambda x: x.strip().split('.'), a))
    c = sorted(b, key=(lambda x: x[0]))
    return c


def ck_format(test_case):
    for i in test_case:
        if len(i) != 2:
            print('有格式错误: ', '.'.join(i))
            return 0
    return 1


def ck_oder(test_case):
    i = len(test_case)-1
    while i >= 0:
        a = test_case[i]
        b = test_case[:i]
        for c in b:
            if a[0] == c[0]:
                print('有序号重复：', '.'.join(a), '  ', '.'.join(c))
                return 0
        i -= 1
    return 1

if __name__ == '__main__':
    with open('testconfig.ini', 'r', encoding='utf-8') as f:
        conf = tools.get_config(f.readlines())
    with open('Testlist.ini', 'r', encoding='utf-8') as f:
        test_lst = f.readlines()

    ts_case = get_case(test_lst)

    if ck_format(ts_case) & ck_oder(ts_case) == 1:
        chrome = webdriver.Chrome()
        for ts in ts_case:
            if ts[1] in D1:
                D1.get(ts[1])(chrome, conf)
        chrome.close()
    else:
        print('22222')

