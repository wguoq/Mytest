# -*- coding:utf-8 -*-
import configparser
import re

import time
from selenium import webdriver
import tools
import script_release


def get_case(test_list):
    a = list(filter(lambda x: re.match('^\d+\.\w+', x), test_list))
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
    chrome = webdriver.Chrome()
    config = configparser.ConfigParser()
    config.read('testconfig.ini', encoding='UTF-8')

    with open('testlist.txt', 'r', encoding='utf-8') as f:
        ts_case = get_case(f.readlines())
        print(ts_case)

    script = {'D1_initialize': (script_release.init, [chrome, config]),
              'D1_login': (script_release.login, [chrome, config]),
              'D1_pppoe': (script_release.pppoe, [chrome, config]),
              'D1_mac_clone': (script_release.mac_clone, [chrome, config]),
              'D1_file_view': (script_release.file_view, [chrome, config]),
              'D1_SSID': (script_release.SSID, [chrome, config])}
    if ck_format(ts_case) & ck_oder(ts_case) == 1:
        test = []
        for t in ts_case:
            if t[1] in script:
                test.append(script.get(t[1]))
            else:
                print(t[1], ' is not in script')
        for func, param in test:
            func(*param)
            time.sleep(60)
    chrome.quit()

