import configparser
import os
import time
from os.path import join
from selenium import webdriver
import Page_script


def check_str(string, ex_lst):
    for ex in ex_lst:
        if string.find(ex) > -1:
            #print('ex==', ex)
            #print('find=  ', string)
            return 0
        else:
            pass
    return 1


def get_folders(folder, exclude_folder):
    file_paths = []
    for paths, dirs, files in os.walk(folder):
        if check_str(paths, exclude_folder) == 1:
            file_paths.append(paths)
    return file_paths


def get_flies(folder):
    file_names = []
    for paths, dirs, files in os.walk(folder):
        file_names.append([(join(paths, name)) for name in files])
    return file_names


def mk_xpath(x):
    return '//a[contains(text(),"{name}")]'.format(name=x)


def file_view_folders(driver, config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='UTF-8')
    samba_ip = config.get('Samba', 'samba_ip')
    samba_pw = config.get('Samba', 'samba_pw')
    drive_letter = config.get('Samba', 'drive_letter')
    first_xp = mk_xpath(config.get('Samba', 'first_folder'))
    exclude = (config.get('Samba', 'exclude')).split(',')
    paths = get_folders(drive_letter, exclude)
    Page_script.open_url(driver, 'http://' + samba_ip)
    Page_script.login(driver, samba_pw)

    for path in paths:
        print(path)
        path = path.split('\\')
        try:
            driver.find_element_by_id("fileview").click()
            time.sleep(5)
            driver.find_element_by_xpath(first_xp).click()
            time.sleep(5)
            for pat in path[1:]:
                pat_xp = mk_xpath(pat)
                driver.find_element_by_xpath(pat_xp).click()
                print('find : ', pat)
                time.sleep(5)
            driver.find_element_by_css_selector("a.setup_return").click()
            time.sleep(5)
        except Exception as e:
            print('can not find: ', path)
            print(e)
    driver.quit()


def file_view_files(driver, config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='UTF-8')
    samba_ip = config.get('Samba', 'samba_ip')
    samba_pw = config.get('Samba', 'samba_pw')
    drive_letter = config.get('Samba', 'drive_letter')
    first_xp = mk_xpath(config.get('Samba', 'first_folder'))
    exclude = (config.get('Samba', 'exclude')).split(',')
    f_names = get_flies(drive_letter)
    Page_script.open_url(driver, 'http://' + samba_ip)
    Page_script.login(driver, samba_pw)

    for names in f_names:
        for name in names:
            if check_str(name, exclude) == 1:
                print(name)
                try:
                    name = name.split('\\')
                    driver.find_element_by_id("fileview").click()
                    time.sleep(5)
                    driver.find_element_by_xpath(first_xp).click()
                    time.sleep(5)
                    for nam in name[1:]:
                        if nam != name[-1]:
                            nam_xp = mk_xpath(nam + '/')
                            driver.find_element_by_xpath(nam_xp).click()
                            time.sleep(5)
                        else:
                            nam_xp = mk_xpath(nam)
                            print('find: ', driver.find_element_by_xpath(nam_xp).text.strip())
                            time.sleep(5)
                    driver.find_element_by_css_selector("a.setup_return").click()
                    time.sleep(5)
                except Exception as e:
                    print('can not find: ', name)
                    print(e)
    driver.quit()


if __name__ == '__main__':
    chrome = webdriver.Chrome()
    file_view_folders(chrome, 'testconfig.ini')
    file_view_files(chrome, 'testconfig.ini')