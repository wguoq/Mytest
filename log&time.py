# -*- coding:utf-8 -*-

import time
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


if __name__ == '__main__':
    logfile = 'serlog.txt'
    lock = threading.RLock()
    a = threading.Thread(target=write_time, args=(logfile, 300))
    b = threading.Thread(target=write_serlog, args=(logfile,))
    threads = [a, b]
    for t in threads:
        t.start()
