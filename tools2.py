
import os
import time
import serial


def ping_ok(ip, n=3):
#调用系统的ping命令
    for i in range(n):
        return1 = os.system('ping -n 1 -w 1 %s' % ip)
        if return1:
            print('ping host fail ip = ', ip)
            time.sleep(5)
        else:
            print('ping ok')
            return 1
    return 0


def getconfig(file):
    line = file.readlines()
    dict2 = dict()
    for l in line:
        l = l.replace(" ", "")
        l = l.replace("\n", "")
        l = l.split("=")
        if len(l) >= 2:
            dict1 = {l[0]: l[1]}
            dict2.update(dict1)
    return dict2


def get_serial_log(com, serlog, lock):
    ser = serial.Serial(port=com, baudrate=115200)
    print(ser.portstr)
    f = open(serlog, "a")
    while 2 > 1:
        data = str(ser.readline())
        if data:
            data = data.replace("\\r", "")
            data = data.replace("\\n", "")
            data = data.replace("b'", "")
            lock.acquire()
            f.write(data + "\n")
            f.flush()
            lock.release()
            print(data)
        else:
            continue
    f.close()


def uci_cmd(ssh_connection, cmd, flag):
    stdin, stdout, stderr = ssh_connection.exec_command(cmd)
    for l in stdout.readlines():
        if l.split('=')[0] == flag:
            return l.split("=")[1]
        else:
            return None
    return None