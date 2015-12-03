# -*- coding:utf-8 -*-
from selenium import webdriver
import Page_script
import re


def initialize():
    print('111initialize')


def login(driver, url, password):
    print('222login')
    Page_script.open_url(driver, url)
    Page_script.login(driver, password)


def pppoe():
    print('333pppoe')


Newifi = {'initialize': initialize,
          'login': login,
          'pppoe': pppoe}



def get_case(test_list):

    for l in test_list:
        if re.match('^\d\.', l):
            print(l)

def ck_lens(test_list):
    if len(test_list) >= 1:
        for l in test_ls:
            if re.match('^\d\.', l):
                return 1
        print('没有有效行')
        return 0
    else:
        print('列表长度为0')
        return 0


def ck_format(test_list):
    test = map(lambda x: x.strip().split('.'), test_list)
    for i in test:
        if len(i) != 2:
            print('格式错误', i)


def ck_oder(test_list):
    i = len(test_list)-1
    while i >= 0:
        ti = test_list[i]
        del test_list[i]
        tt = []+test_list
        for t in tt:
            if ti[0] == t[0]:
                print('有序号重复：\n', ti, t)
                return 0
        i -= 1
    return 1

if __name__ == '__main__':
    # chrome = webdriver.Chrome()
    test_url = 'http://192.168.99.1'
    pw = '12345678'

    with open('Testlist.ini', 'r', encoding='utf-8') as f:
        test_ls = f.readlines()

    ck_format(test_ls)