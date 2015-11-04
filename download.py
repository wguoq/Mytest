import os
import random
import paramiko

__author__ = 'hello'
import requests
import paramiko
import json
import time
import webbrowser

pan = "http://www.baidu.com"


def down(url):
    with open('file.zip', 'wb') as f:
        try:
            print("======start download======")
            st = time.time()
            f.write(requests.get(url).content)
            end = time.time()
            print("======download success======")
            t = '%.2f' % ((end - st)*1000)
            return ['success', os.path.getsize('file.zip'), t]
        except Exception as e:
            print("======download fail======")
            return ['fail', 'error:'+str(e), '0']


#print(down(pan))


def get_html(url):
    try:
        print("======start======")
        st = time.time()
        f = requests.get(url).text
        end = time.time()
        print("======success======")
        #print(f)
        t = '%.2f' % ((end - st)*1000)
        return ['success', f, t]
    except Exception as e:
        print("======fail======")
        return ['fail', "error:"+str(e), '0']

#print(get_html(pan))

data = ''
while 2 > 1:
    url = open("10url", 'r').readlines()
    for l in url:
        l = l.strip()
        print(l)
        a = get_html(l)
        if a[0] == 'success':
            print(a[2])
            data = data+'\t'+l+'\t'+a[2]
        if a[0] == 'fail':
            print(a[1])
            data = data+'\t'+l+'\t'+a[2]
        time.sleep(1)
    f = open('ttt.txt', 'a')
    f.write(data + '\n')
    f.close()
    data = ''



