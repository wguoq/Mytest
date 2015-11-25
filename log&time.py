# -*- coding:utf-8 -*-

import time
import paramiko
import tools
import serial
import threading


def write_time(filename, delay=120):
    f = open(filename, 'a')
    while True:
        date = time.ctime(time.time())
        lock.acquire()
        tools.write_ser_log(date, f)
        lock.release()
        time.sleep(delay)
    f.close()


def write_serlog(filename, port='COM3', baudrate=115200):
    ser = serial.Serial(port, baudrate)
    f = open(filename, 'a')
    while True:
        log = str(ser.readline())
        lock.acquire()
        tools.write_ser_log(log, f)
        lock.release()
    f.close()


def write_sshlog(ssh, sshcmd, sshlog):
    f = open(sshlog, 'a')
    while True:
        f.write(time.ctime(time.time())+'\n')
        ssh.connect("192.168.99.1", 22, "root", "12345678")
        stdin, stdout, stderr = ssh.exec_command(sshcmd)
        cmd_log = stdout.readlines()
        ssh.close()
        for l in cmd_log:
            print(str(l))
            f.write(str(l)+'\n')
            f.flush()
        f.write('\n')
        time.sleep(30)
    f.close()

if __name__ == '__main__':
    logfile = 'serlog.txt'
    ssh_log = 'sshlog.txt'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cmd = 'ps'
    lock = threading.RLock()
    a = threading.Thread(target=write_time, args=(logfile, 1800))
    b = threading.Thread(target=write_serlog, args=(logfile,))
    c = threading.Thread(target=write_sshlog, args=(ssh, cmd, ssh_log))
    threads = [a, b, c]
    for t in threads:
        t.start()
