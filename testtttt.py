from os.path import join
from selenium import webdriver
import Page_script
import unittest, time, re, os
import configparser

config = configparser.ConfigParser()
config.read("TestConfig.ini", encoding='UTF-8')
drive_letter = config.get('Samba', 'drive_letter')
first_folder = config.get('Samba', 'first_folder')
exclude = config.get('Samba', 'exclude')


def check_str(string, ex_lst):
    for ex in ex_lst:
        if string.find(ex) > -1:
            #print('ex==', ex)
            #print('find=  ', string)
            return 0
        else:
            pass
    return 1


def walk_folder(folder):
    file_paths = []
    file_names = []
    for paths, dirs, files in os.walk(folder):
        if check_str(paths, exclude.split(',')) == 1:
            file_paths.append(paths)
        file_names.append([(join(paths, name)) for name in files])
    return file_paths, file_names


def mk_xpath(x):
    f = '//a[contains(text(),"{name}")]'.format(name=x)
    return f


f_path, f_names = walk_folder(drive_letter)
driver = webdriver.Chrome()
driver.get('http://192.168.99.1')
Page_script.login(driver, '12345678')
time.sleep(3)
first_xp = mk_xpath(first_folder)

'''
for path in f_path:
    path = path.split('\\')
    print(path)
    try:
        driver.find_element_by_id("fileview").click()
        time.sleep(3)
        driver.find_element_by_xpath(first_xp).click()
        time.sleep(3)
        for pat in path[1:]:
            pat_xp = mk_xpath(pat)
            driver.find_element_by_xpath(pat_xp).click()
            time.sleep(3)
        driver.find_element_by_css_selector("a.setup_return").click()
        time.sleep(3)
    except Exception as e:
        print(e)
'''
for names in f_names:
    for name in names:
        if check_str(name, exclude.split(',')) == 1:
            name = name.split('\\')
            print(name)
            driver.find_element_by_id("fileview").click()
            time.sleep(3)
            driver.find_element_by_xpath(first_xp).click()
            time.sleep(3)
            for nam in name[1:]:
                if nam != name[-1]:
                    nam_xp = mk_xpath(nam + '/')
                    driver.find_element_by_xpath(nam_xp).click()
                    time.sleep(3)
                else:
                    nam_xp = mk_xpath(nam)
                    print(driver.find_element_by_xpath(nam_xp).text)
                    time.sleep(3)
            driver.find_element_by_css_selector("a.setup_return").click()
            time.sleep(3)

driver.quit()
