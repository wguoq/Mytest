import time
import paramiko
import tools
import script_page


def init(driver, url, config):
    print('D1_initialize')
    time.sleep(5)
    password = config.get('admin_pw')
    username = config.get('pppoe_user')
    pw = config.get('pppoe_pwd')
    script_page.open_url(driver, url)
    if script_page.initialize(driver, url, password, username, pw) == 1:
        print('init success')
    else:
        print('init fail!!!')


def login(driver, url, password):
    print('D1_login')
    time.sleep(5)
    script_page.open_url(driver, url)
    if script_page.login(driver, password) == 1:
        print('login success')
    else:
        print('login fail!!!')


def pppoe(driver, url, config):
    print('D1_pppoe')
    time.sleep(5)
    password = config.get('admin_pw')
    user = config.get('pppoe_user')
    pw = config.get('pppoe_pwd')
    script_page.open_url(driver, url)
    script_page.login(driver, password)
    if script_page.connect_pppoe(driver, user, pw) == 1:
        print('pppoe connect success')
    else:
        print('pppoe connect fail!!!')


def mac_clone(driver, url, password):
    print('D1_mac_clone')
    time.sleep(5)
    script_page.open_url(driver, url)
    script_page.login(driver, password)
    cur_mac = script_page.clone_cur_mac(driver)
    a = ['a']
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.99.1', port=22, username='root', password=password)
        stdin, stdout, stderr = ssh.exec_command('ifconfig eth0.2')
        a = tools.find_flag(stdout, 'HWaddr')
        ssh.close()
    except Exception as e:
        print(e)
    HWaddr = str(a[0])
    if cur_mac == HWaddr[HWaddr.find('HWaddr')+len('HWaddr'):].lower().strip():
        print('mac clone success')
    else:
        print('mac clone fail!!!')

