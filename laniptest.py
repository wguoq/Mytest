# -*- coding:utf-8 -*-
import XcloudScript
from selenium import webdriver
import time

chrome = webdriver.Chrome()
a = 99
b = 98
for i in range(99):
    print(i)
    ip1 = '192.168.'+str(a)+'.1'
    url = 'http://'+ip1
    print('111 '+ip1)
    #print('222 '+url)
    ip2 = '192.168.'+str(b)+'.1'
    print('333 '+ip2)
    try:
        XcloudScript.open_url(chrome, url)
        time.sleep(2)
        XcloudScript.login(chrome, "12345678")
        time.sleep(2)
        chrome.find_element_by_id("lan").click()
        time.sleep(10)
        chrome.find_element_by_css_selector("input.lansetuppart1_input.ipads").clear()
        time.sleep(1)
        chrome.find_element_by_css_selector("input.lansetuppart1_input.ipads").send_keys(ip2)
        time.sleep(1)
        chrome.find_element_by_id("lansetuppart1_save").click()
        a, b = b, a
        time.sleep(200)
    except Exception as e:
        print(e)
        time.sleep(200)