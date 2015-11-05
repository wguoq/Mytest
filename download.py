import os
import requests
import time


qq = "http://dldir1.qq.com/qqfile/qq/QQ7.8/16379/QQ7.8.exe"


def download(download_url):
    with open('file.zip', 'wb') as f:
        try:
            st = time.time()
            f.write(requests.get(download_url).content)
            end = time.time()
            t = '%.2f' % ((end - st)*1000)
            return ['success', os.path.getsize('file.zip'), t]
        except Exception as e:
            return ['fail', 'error:'+str(e), '0']
        finally:
            f.close()


def get_html(html_url):
    try:
        st = time.time()
        text = requests.get(html_url).text
        end = time.time()
        t = '%.2f' % ((end - st)*1000)
        return ['success', text, t]
    except Exception as e:
        return ['fail', "error:"+str(e), '0']


def dotest():
    f = open('ttt.txt', 'a')
    while 2 > 1:
        op = open('10url', 'r')
        url = op.readlines()
        op.close()
        for l in url:
            l = l.strip()
            a = get_html(l)
            time.sleep(2)
            data = l+'\t'+a[2]
            print(data)
            f.write(data+'\n')
            f.flush()
    f.close()


def dotest2():
    f = open('ttt.txt', 'a')
    while 2 > 1:
        print('downloading')
        a = download(qq)
        data = a[0]+'\t'+a[1]+'\t'+a[2]
        print(data)
        f.write(data)
        f.flush()
        time.sleep(5)
    f.close()

dotest2()

