
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


def dotest(cmd, delay):
    while 2 > 1:
        time.sleep(delay)
        f = open("123.txt", "a")
        try:
            stdin, stdout, stderr = ssh.exec_command(cmd[0])
            lst = stdout.readlines()
            a = json.JSONDecoder().decode(''.join(lst))
            f.write(time.ctime(time.time())+"\t"+str(a.get(cmd[1]))+"\t"+str(a.get(cmd[2]))+"\n")
            print(a)
        except Exception as e:
            print(e)
        finally:
            f.close()


def dotest2(cmd, delay):
    while 2 > 1:
        time.sleep(delay)
        with open('hangzhang.txt', 'a') as f:
            try:
                date = time.ctime(time.time())
                stdin, stdout, stderr = ssh.exec_command(cmd[0])
                lst1 = stdout.readlines()
                stdin, stdout, stderr = ssh.exec_command(cmd[1])
                lst2 = stdout.readlines()
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
                    data = data1+'\t'+x[0]+'\t'+x[1]+'\t'+x[2]+'\n'
                    print(data)
                    f.write(data)
            except Exception as e:
                print(e)
            finally:
                f.close()


dotest2(ip_rate, 15)

