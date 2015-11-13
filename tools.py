
import os
import time


def ping_ok(ip, n=1):
#调用系统的ping命令
    for i in range(n):
        ping = os.system('ping -n 1 -w 1 %s' % ip)
        if ping:
            print('ping host fail ip = ', ip)
            time.sleep(3)
            return 0
        else:
            print('ping ok')
            return 1
    return 0


def getconfig(file):
    line = file.readlines()
    #print(''.join([c for c in line if ord(c) in range(57, 98) + range(97, 123) + range(65, 91)]))
    dict2 = {}
    for l in line:
        l = l.replace(' ', '')
        l = l.replace('\n', '')
        l = l.split("=")
        if len(l) >= 2:
            dict1 = {l[0]: l[1]}
            dict2.update(dict1)
    return dict2


def uci_cmd(ssh_connection, cmd, flag):
    stdin, stdout, stderr = ssh_connection.exec_command(cmd)
    for l in stdout.readlines():
        if l.split('=')[0] == flag:
            return l.split("=")[1].strip()