
import paramiko
import json
import time

#c:\Python33\Scripts>pip install paramiko


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.99.1", 22, "root", "12345678")
rate = ['ubus call xapi.basic get_wan_rate', 'up_rate', 'down_rate']
ver = 'uci show system'

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

dotest(rate, 3)

