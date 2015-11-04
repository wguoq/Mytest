__author__ = 'hello'
import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.99.1', 22, 'root', '12345678')
o = 0
while 2 > 1:
    for i in range(14):
        try:
            i += 1
            cmd = 'uci set wireless.ra0.channel='+str(i)
            print(o)
            print(cmd)
            o += 1
            ssh.exec_command(cmd)
            time.sleep(2)
            ssh.exec_command('uci commit wireless')
            print('uci commit wireless')
            time.sleep(2)
            ssh.exec_command('wifi up ra0')
            print('wifi up ra0')
            time.sleep(60)
        except Exception as e:
            print(e)
