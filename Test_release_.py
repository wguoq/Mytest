# -*- coding:utf-8 -*-
################################
# release test 脚本
# 在testconfig.ini里面配置各种环境参数
# 在testlist.txt里面配置各个测试用例的执行顺序
# 注意配置测试用例名称和方法的对应关系
################################

import configparser
import re
import time
from selenium import webdriver
import script_release
import logging


if __name__ == '__main__':
    def get_case(test_list):
        a = list(filter(lambda x: re.match('^\d+\.\w+', x), test_list))
        b = list(map(lambda x: x.strip().split('.'), a))
        c = sorted(b, key=(lambda x: x[0]))
        return c

    def ck_format(test_case):
        for i in test_case:
            if len(i) != 2:
                logging.warning('格式错误: ', '.'.join(i))
                return 0
        return 1

    def ck_oder(test_case):
        i = len(test_case) - 1
        while i >= 0:
            a = test_case[i]
            b = test_case[:i]
            for c in b:
                if a[0] == c[0]:
                    logging.warning('序号重复：', '.'.join(a), '  ', '.'.join(c))
                    return 0
            i -= 1
        return 1

    #记录日志的级别：DEBUG,INFO,WARN,ERROR
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s:\n%(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='release_test.log',
                        filemode='a',
                        encoding='UTF-8')
    #将INFO级别以上的日志信息打印到console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s:   %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    #读取配置文件
    config = configparser.ConfigParser()
    config.read('testconfig.ini', encoding='UTF-8')
    with open('testlist.txt', 'r', encoding='utf-8') as f:
        ts_case = get_case(f.readlines())
    logging.info(ts_case)
    chrome = webdriver.Chrome()
    #定义testlist中测试用例名字和实际调用方法的对应关系以及其参数
    script = {'D1_initialize': (script_release.init_config, [chrome, config]),
              'D1_login': (script_release.login, [chrome, config]),
              'D1_pppoe': (script_release.pppoe, [chrome, config]),
              'D1_mac_clone': (script_release.mac_clone, [chrome, config]),
              'D1_file_view': (script_release.file_view, [chrome, config]),
              'D1_SSID': (script_release.set_ssid, [chrome, config]),
              'D1_set_pwd': (script_release.new_password, [chrome, config]),
              'D1_QOS': (script_release.qos, [chrome, config])}
    #检查配置文件格式是否正确
    if ck_format(ts_case) & ck_oder(ts_case) == 1:
        test = []
        for t in ts_case:
            if t[1] in script:
                test.append(script.get(t[1]))
            else:
                logging.warning(str(t) + ' is not in script')
        for func, param in test:
            #运行测试方法
            func(*param)
            time.sleep(10)
    chrome.quit()
