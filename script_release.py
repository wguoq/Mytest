import time
import paramiko
import tools
import script_page
import Test_file_view


def init(driver, configparser):
    print('D1_initialize')
    time.sleep(5)
    default_ip = configparser.get('Default', 'default_ip')
    default_pw = configparser.get('Default', 'default_pw')
    pppoe_user = configparser.get('PPPOE', 'pppoe_user')
    pppoe_pwd = configparser.get('PPPOE', 'pppoe_pwd')
    if script_page.initialize(driver, 'http://'+default_ip, default_pw, pppoe_user, pppoe_pwd) == 1:
        print('init success')
    else:
        print('init fail!!!')


def login(driver, configparser):
    print('D1_login')
    time.sleep(5)
    default_ip = configparser.get('Default', 'default_ip')
    default_pw = configparser.get('Default', 'default_pw')
    script_page.open_url(driver, 'http://'+default_ip)
    if script_page.login(driver, default_pw) == 1:
        print('login success')
    else:
        print('login fail!!!')


def pppoe(driver, configparser):
    print('D1_pppoe')
    time.sleep(5)
    pppoe_ip = configparser.get('PPPOE', 'pppoe_ip')
    pppoe_pw = configparser.get('PPPOE', 'pppoe_pw')
    pppoe_user = configparser.get('Default', 'pppoe_user')
    pppoe_pwd = configparser.get('Default', 'pppoe_pwd')
    script_page.open_url(driver, 'http://'+pppoe_ip)
    script_page.login(driver, pppoe_pw)
    if script_page.connect_pppoe(driver, pppoe_user, pppoe_pwd) == 1:
        print('pppoe connect success')
    else:
        print('pppoe connect fail!!!')


def mac_clone(driver, configparser):
    print('D1_mac_clone')
    time.sleep(5)
    default_ip = configparser.get('Default', 'default_ip')
    default_pw = configparser.get('Default', 'default_pw')
    script_page.open_url(driver, 'http://'+default_ip)
    script_page.login(driver, default_pw)
    cur_mac = script_page.clone_cur_mac(driver)
    a = ['a']
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.99.1', port=22, username='root', password=default_pw)
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


def file_view(driver, configparser):
    Test_file_view.file_view_folders(driver, configparser)
    Test_file_view.file_view_files()