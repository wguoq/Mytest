# -*- coding:utf-8 -*-
import configparser
import re
import time
from selenium import webdriver
import tools
import script_release
import logging


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
    config = configparser.ConfigParser()
    config.read('testconfig.ini', encoding='UTF-8')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='release.log',
                        filemode='a',
                        encoding='UTF-8')
    #################################################################################################
    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:   %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    #################################################################################################
    chrome = webdriver.Chrome()
    with open('testlist.txt', 'r', encoding='utf-8') as f:
        ts_case = get_case(f.readlines())
    print(ts_case)

    script = {'D1_initialize': (script_release.init_config, [chrome, config]),
              'D1_login': (script_release.login, [chrome, config]),
              'D1_pppoe': (script_release.pppoe, [chrome, config]),
              'D1_mac_clone': (script_release.mac_clone, [chrome, config]),
              'D1_file_view': (script_release.file_view, [chrome, config]),
              'D1_SSID': (script_release.set_ssid, [chrome, config])}

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
