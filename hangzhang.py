
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
pid = 'cat /proc/pid_flow'


def dotest2(cmd, delay):
    f = open('hangzhang.txt', 'a')
    first = 'time'+'\t'+'all up'+'\t'+'all down'+'\t'+'host'+'\t'+'host up'+'\t'+'host down'+'\n'
    f.write(first)
    f.flush()
    while 2 > 1:
        time.sleep(delay)
        try:
            date = time.ctime(time.time())
            stdin, stdout, stderr = ssh.exec_command(cmd[1])
            lst2 = stdout.readlines()
            stdin, stdout, stderr = ssh.exec_command(cmd[0])
            lst1 = stdout.readlines()
            a = json.JSONDecoder().decode(''.join(lst2))
            up = str(a.get('up_rate'))
            down = str(a.get('down_rate'))
            data1 = date+'\t'+up+'\t'+down
            ip = ''
            ip_up = 0
            ip_down = 0
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
            f.write(data)
            f.flush()
        except Exception as e:
            print(e)
    f.close()

dotest2(ip_rate, 5)

