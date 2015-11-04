# -*- coding:utf-8 -*-

import requests
import re
import time


api = "http://online-api.xcloud.cc/router/smac?mac="

f = open("MAC", "r")
macREX = r"smac': '([a-zA-Z0-9]+)'}"
x = 0
while f:
    l = f.readline()
    print(l)
    x += 1
    maclist = l.split("\t")
    if len(maclist) > 1:
        time.sleep(0.5)
        oldmac = maclist[0].replace("\n", "")
        newmac = maclist[1].replace("\n", "")

        url = api + oldmac
        r = requests.get(url).json()

        a = re.compile(macREX).findall(str(r))[0]

        if a == newmac:
            print(x)
            print(newmac+"=="+a)
            print("success")
        else:
            print("fail")
            print(newmac+"!=="+a)
    else:
        print("121212121")
        break











