# -*- coding:utf-8 -*-

import time
import tools
import serial
import threading


def write_time(filename, delay=300):
    while True:
        date = time.ctime(time.time())
        lock.acquire()
        tools.write_ser_log(date, filename)
        lock.release()
        time.sleep(delay)


def write_serlog(filename, port='COM3', baudrate=115200):
    ser = serial.Serial(port, baudrate)
    while True:
        log = str(ser.readline())
        lock.acquire()
        tools.write_ser_log(log, filename)
        lock.release()

if __name__ == '__main__':
    logfile = 'serlog.txt'
    lock = threading.RLock()
    a = threading.Thread(target=write_time, args=(logfile, 300))
    b = threading.Thread(target=write_serlog, args=(logfile,))
    threads = [a, b]
    for t in threads:
        t.start()