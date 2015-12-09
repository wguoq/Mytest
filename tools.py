import os
import time


def ping_ok(ip, n=3):
    for i in range(n):
        re = os.system('ping -n 1 -w 1 %s' % ip)
        if re:
            print('ping host fail ip = ', ip)
            time.sleep(1)
        else:
            print('ping ok')
            return 1
    return 0


def get_config(lines):
    d = {}
    for i in list(map(lambda x: x.strip().split('='), lines)):
        if len(i) == 2:
            d.update({i[0]: i[1]})
    return d


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
            pass
    return None


def find_flag(lines, flag):
    return [l for l in lines if l.find(flag) > -1]
