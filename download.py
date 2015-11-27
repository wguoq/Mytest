# -*- coding:utf-8 -*-
import threading
import time
import urllib.request
import sys
import logging
import socket
import random

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='qq.log',
                    filemode='a')
#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################



baidu = 'https://www.baidu.com/img/bd_logo1.png'
baiqq = 'http://dlsw.baidu.com/sw-search-sp/soft/3a/12350/QQ_7.8.16379.0_setup.1446522220.exe'

socket.setdefaulttimeout(60)


def report(blockCount, blockSize, totalSize):
    percent = int(blockCount*blockSize*100/totalSize)
    sys.stdout.write("\r%d%%" % percent + ' complete ')
    sys.stdout.flush()


def download(url, localfile='temp'):
    size = 0
    url = url.strip()
    try:
        s = time.time()
        result = urllib.request.urlretrieve(url, localfile, reporthook=report)
        e = time.time()
        t = e - s
        headers = result[1]
        if 'Content-Length' in headers:
            size = int(headers['Content-Length'])
        return {'result': 'success', 'localfile': localfile, 'size': size, 'time': t}
    except Exception as e:
        return {'result': e, 'localfile': None, 'size': 0, 'time': 0}


def dotest(url, delay=60):
    #while True:
    print(time.ctime(time.time()))
    print('start download')
    data = download(url)
    if data.get('result') == 'success':
        size = round(data.get('size')/1024, 2)
        t = round(data.get('time'), 2)
        speed = round(size/t, 2)
        logging.info(data.get('localfile')+'\t'+str(size)+'KB'+'\t'+str(t)+'s'+'\t'+str(speed)+'KB/s')
    else:
        logging.warning(data.get('result'))
    time.sleep(delay)

while True:
    dotest(baiqq, random.randint(60, 120))

'''
for i in range(1000):
    ti = threading.Thread(target=do_test, args=(baidu, 10))
    ti.start()
'''
