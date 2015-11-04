
import paramiko
import json
import time

#c:\Python33\Scripts>pip install paramiko


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.99.1", 22, "root", "12345678")
rate = ['ubus call xapi.basic get_wan_rate', 'up_rate', 'down_rate']
ver = 'uci show system'
ip_rate = ['cat /proc/ip_rate/list', 'ubus call xapi.basic get_wan_rate']

def dotest(cmd, delay):
    while 2 > 1:
        time.sleep(delay)
        try:
            n = time.time()
            stdin, stdout, stderr = ssh.exec_command(cmd[0])
            m = time.time()
            b = '%.4f' % ((m - n)*1000)
            lst = stdout.readlines()
            a = json.JSONDecoder().decode(''.join(lst))
            f = open("123.txt", "a")
            f.write(time.ctime(time.time()) + "\t" + str(a.get(cmd[1])) + "\t" + str(a.get(cmd[2])) + "\n")
            f.close()
            print(a)
        except Exception as e:
            print(e)

#dotest(rate, 3)

def dotest2(cmd, delay):
    data = ''
    while 2 > 1:
        time.sleep(delay)
        try:
            date = time.ctime(time.time())
            stdin, stdout, stderr = ssh.exec_command(cmd[0])
            lst1 = stdout.readlines()
            stdin, stdout, stderr = ssh.exec_command(cmd[1])
            lst2 = stdout.readlines()
            a = json.JSONDecoder().decode(''.join(lst2))
            allup = str(a.get('up_rate'))
            alldown = str(a.get('down_rate'))
            data = data + '\t' + date + '\t'+ allup + '\t' + alldown
            for x in lst1[1:]:
                x = x.split(' ')
                data = data + '\t' + x[0] + '\t' + x[1] + '\t' + x[2] + '\n'
            print(data)
            f = open('hangzhang.txt', 'a')
            f.write(data)
            f.close()
            data = ''
        except Exception as e:
            print(e)

dotest2(ip_rate, 15)
