__author__ = 'hello'
import time
from selenium import webdriver


def open_url(whitelist):
    for i in whitelist:
        driver = webdriver.Chrome()
        x = i.replace("\"", "")
        print(x)
        try:
            driver.get(x)
            time.sleep(10)
            driver.close()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    for i in range(100):
        file = open('JDwhiteList', 'r')
        l = file.readlines()
        file1 = open('JDwhiteList1', 'r')
        l1 = file1.readlines()
        file2 = open('JDwhiteList2', 'r')
        l2 = file2.readlines()
        file3 = open('JDwhiteList3', 'r')
        l3 = file3.readlines()
        file4 = open('JDwhiteList4', 'r')
        l4 = file4.readlines()
        file5 = open('JDwhiteList5', 'r')
        l5 = file5.readlines()
        file6 = open('JDwhiteList6', 'r')
        l6 = file6.readlines()
        file7 = open('JDwhiteList7', 'r')
        l7 = file7.readlines()
        open_url(l)

