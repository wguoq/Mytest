# -*- coding=utf-8 -*-
import contextlib
import threading
import time
import urllib.request
import sys
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='down.log',
                    filemode='w')
#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


qq = "http://dldir1.qq.com/qqfile/qq/QQ7.8/16379/QQ7.8.exe"
tudou = 'http://tudou.com'
local = 'http://127.0.0.1/180.zip'
d1 = 'http://dteamwebtmpdns.trafficmanager.cn/public/upload/20151103/xCloudOS_newifi-d1_Build20151027_v0.0.4.8100_beta_sign.bin'
baidu = 'https://www.baidu.com/img/bd_logo1.png'


def report(blockCount, blockSize, totalSize):
    percent = int(blockCount*blockSize*100/totalSize)
    sys.stdout.write("\r%d%%" % percent + ' complete ')
    sys.stdout.flush()


def download(url, localfile='temp'):
    size = 0
    try:
        with contextlib.closing(urllib.request.urlopen(url, data=None)) as fp:
            headers = fp.info()
            #print(headers)
            if "content-length" in headers:
                size = int(headers["Content-Length"])
        s = time.time()
        urllib.request.urlretrieve(url, localfile, reporthook=report)
        e = time.time()
        t = e - s
        return {'result': 'success', 'localfile': localfile, 'size': size, 'time': t}
    except Exception as e:
        return {'result': e, 'localfile': None, 'size': 0, 'time': 0}


def dotest(url, delay=0):
    while True:
        data = download(url)
        #print(data)
        if data.get('result') == 'success':
            size = round(data.get('size')/1024, 2)
            #print(size)
            t = round(data.get('time'), 2)
            #print(t)
            speed = round(size/t, 2)
            #print(speed)
            logging.info(data.get('localfile')+'\t'+str(size)+'KB'+'\t'+str(t)+'s'+'\t'+str(speed)+'KB/s')
        else:
            logging.warning(data.get('result'))
        time.sleep(delay)


a = threading.Thread(target=dotest, args=(qq, 360,))
#a.start()

for i in range(10000):
    ti = threading.Thread(target=dotest, args=(baidu, 1,))
    ti.start()
