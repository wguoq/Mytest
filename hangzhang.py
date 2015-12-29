#c:\Python33\Scripts>pip install paramiko
#把TF卡映射成X盘

import paramiko
import json
import time


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.99.1", 22, "root", "12345678")
rate = ['ubus call xapi.basic get_wan_rate', 'up_rate', 'down_rate']
ip_rate = \
    ['cat /proc/ip_rate/list > /mnt/mmcblk0p1//log1.txt;ubus call xapi.basic get_wan_rate > /mnt/mmcblk0p1//log2.txt']
log1 = 'X:\log1.txt'
log2 = 'X:\log2.txt'


def do_test(cmd, delay):
    hz = open('hangzhang.txt', 'a')
    first_line = 'time'+'\t'+'all up'+'\t'+'all down'+'\t'+'host'+'\t'+'host up'+'\t'+'host down'+'\n'
    hz.write(first_line)
    hz.flush()
    while True:
        time.sleep(delay)
        ip = ''
        ip_up = 0
        ip_down = 0
        date = time.ctime(time.time())
        try:
            ssh.exec_command(cmd[0])
            time.sleep(3)
            with open(log1, 'r', encoding='utf-8') as f1:
                lst1 = f1.readlines()
            with open(log2, 'r', encoding='utf-8') as f2:
                lst2 = f2.readlines()
        except Exception as e:
            print(e)
            continue
        a = json.JSONDecoder().decode(''.join(lst2))
        up = str(a.get('up_rate'))
        down = str(a.get('down_rate'))
        data1 = date+'\t'+up+'\t'+down
        for x in lst1[1:]:
            x = x.split(' ')
            if x[0] is None:
                x[0] = 0
            if x[1] is None:
                x[1] = 0
            if x[2] is None:
                x[2] = 0
            ip = ip+' '+x[0]
            ip_up += int(x[1])
            ip_down += int(x[2])
        data = data1+'\t'+ip+'\t'+str(ip_up)+'\t'+str(ip_down)+'\n'
        print(data)
        hz.write(data)
        hz.flush()
    hz.close()

do_test(ip_rate, 60)

