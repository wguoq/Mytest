import logging

__author__ = 'hello'

import paramiko
import json
import time
import threading

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='ubus.log',
                    filemode='w')
#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.99.1", 22, "root", "12345678")
wan = ['ubus call xapi.basic get_wan_conn_info', 'wan_ip', {'dns2': '114.114.114.114', 'wan_uptime': '00H18M46S', 'dns1': '61.139.2.69', 'wan_ip': '192.168.102.183', 'wan_proto': 'dhcp', 'wan_gateway': '192.168.102.254'}]
lan = ["ubus call xapi.basic get_lan_ip", 'macaddr', {'ipaddr': '192.168.99.1', 'EncryptMacaddr': 'EB217D55CB39E650E6CD6AB4396153639C08F109713C7F40D445EE58F0075BBB', 'netmask': '255.255.255.0', 'macaddr': '70:25:59:fd:d0:d6'}]
usb = ["ubus call xapi.basic get_state_of_storage_device", 'USED_STATE', {'all_state': [{'TIME': '1446019097', 'STATE': '1', 'NAME': '/dev/mmcblk0p1', 'TYPE': 'ext4', 'ID': '1', 'SIZE': '7449528', 'USED_STATE': '-1', 'VENDOR': 'unknown', 'UUID': 'f2e9f4ec-6e05-4ec1-b832-7876b9721e7c', 'MOUNT_DIR': '/mnt/mmcblk0p1', 'X_SOURCE': '1', 'FREE': '3879984', 'LABEL': '', 'TRANSFER_LABEL': '0', 'S_CHANGE_TIME': '1446189825'}]}]
ver = ["ubus call xapi.basic get_version", 'distrib_release', {'distrib_codename': 'beta', 'distrib_platform': 'newifi-d1', 'status': 0, 'distrib_release': '0.0.4.8600', 'distrib_id': 'xCloudOS'}]


def dolog(file, s):
    file.write(s + "\n")


def dotest(cmd, delay, func):
    f = open(cmd[0], "a")
    func(f, time.ctime(time.time()))
    for i in range(5):
        time.sleep(delay)
        try:
            n = time.time()
            stdin, stdout, stderr = ssh.exec_command(cmd[0])
            m = time.time()
            b = '%.4f' % ((m - n)*1000)
            print(b)
            f.write(b + "\n")
            f.flush()
            lst = stdout.readlines()
            a = json.JSONDecoder().decode(''.join(lst))
            #print(a)
            if a.get(cmd[1]) == (cmd[2].get(cmd[1])):
                logging.info(i)
                logging.info("success")
            else:
                logging.info(i)
                logging.info("time out")
        except Exception as e:
            logging.error(e)
    func(f, time.ctime(time.time()))
    f.close()

#dotest(usb, 1)

t1 = threading.Thread(target=dotest, args=(wan, 3, dolog))
t2 = threading.Thread(target=dotest, args=(lan, 3, dolog))
t3 = threading.Thread(target=dotest, args=(usb, 3, dolog))
t4 = threading.Thread(target=dotest, args=(ver, 3, dolog))

threads = [t1, t2, t3, t4]
#t1.start()

for t in threads:
    t.start()