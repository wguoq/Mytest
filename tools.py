import os
import time


def ping_ok(ip, n=3):
    # 调用系统的ping命令
    for i in range(n):
        return1 = os.system('ping -n 1 -w 1 %s' % ip)
        if return1:
            print('ping host fail ip = ', ip)
            time.sleep(5)
        else:
            print('ping ok')
            return 1
    return 0


def get_config(file):
    line = file.readlines()
    dict2 = dict()
    for l in line:
        l = l.strip()
        l = l.split("=")
        if len(l) >= 2:
            dict1 = {l[0]: l[1]}
            dict2.update(dict1)
    return dict2


def write_ser_log(log, file):
    if None != log:
        log = log.replace("\\r", "")
        log = log.replace("\\n", "")
        log = log.replace("b'", "")
        log = log.replace("'", "")
        log = log.strip()
        file.write(log + "\n")
        file.flush()
        print(log)
    else:
        pass


def uci_cmd(ssh_connection, cmd, flag):
    stdin, stdout, stderr = ssh_connection.exec_command(cmd)
    for l in stdout.readlines():
        if l.split('=')[0] == flag:
            return l.split("=")[1]
        else:
            return None
    return None