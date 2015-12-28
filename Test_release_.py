# -*- coding:utf-8 -*-
import re
from selenium import webdriver
import tools




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
    with open('testconfig.ini', 'r', encoding='utf-8') as f:
        conf = tools.get_config(f.readlines())
        admin_pw = conf.get('admin_pw')
        default_url = 'http://'+conf.get('default_ip')
    with open('testlist.txt', 'r', encoding='utf-8') as f:
        ts_case = get_case(f.readlines())
        print(ts_case)

    script = {'D1_initialize': (init, [chrome, default_url, conf]),
              'D1_login': (login, [chrome, default_url, admin_pw]),
              'D1_pppoe': (pppoe, [chrome, default_url, conf]),
              'D1_mac_clone': (mac_clone, [chrome, default_url, admin_pw])}

    if ck_format(ts_case) & ck_oder(ts_case) == 1:
        test = []
        for t in ts_case:
            if t[1] in script:
                test.append(script.get(t[1]))
        for func, param in test:
            func(*param)
    else:
        print('22222')
    chrome.close()

