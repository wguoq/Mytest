import os
import time
import requests
import urllib.request
import script_page
import Test_file_view
import logging


def init_config(driver, config_parser):
    logging.info('D1_initialize 不插网线/DHCP/拨号都支持，完成配置进入首页算成功')
    default_ip = config_parser.get('Default', 'default_ip')
    default_pw = config_parser.get('Default', 'default_pw')
    pppoe_user = config_parser.get('PPPOE', 'pppoe_user')
    pppoe_pwd = config_parser.get('PPPOE', 'pppoe_pwd')
    logging.debug(' default_ip=' + str(default_ip) + '\n' +
                  ' default_pw=' + str(default_pw) + '\n' +
                  ' pppoe_user=' + str(pppoe_user) + '\n' +
                  ' pppoe_pwd=' + str(pppoe_pwd)
                  )
    if script_page.initialize(driver, 'http://' + default_ip, default_pw, pppoe_user, pppoe_pwd) == 1:
        logging.info('test init_config success')
    else:
        logging.warning('test init_config fail!!!')


def login(driver, config_parser):
    logging.info('D1_login 输入密码，进入首页算成功')
    default_ip = config_parser.get('Default', 'default_ip')
    default_pw = config_parser.get('Default', 'default_pw')
    logging.debug(' default_ip=' + str(default_ip) + '\n' +
                  ' default_pw=' + str(default_pw))
    script_page.open_url(driver, 'http://' + default_ip)
    if script_page.login(driver, default_pw) == 1:
        logging.info('test login success')
    else:
        logging.warning('test login fail!!!')


def pppoe(driver, config_parser):
    logging.info('D1_pppoe 输入账号密码拨号，页面返回连接成功就算成功，不验证是否上网')
    pppoe_ip = config_parser.get('PPPOE', 'pppoe_ip')
    pppoe_pw = config_parser.get('PPPOE', 'pppoe_pw')
    pppoe_user = config_parser.get('PPPOE', 'pppoe_user')
    pppoe_pwd = config_parser.get('PPPOE', 'pppoe_pwd')
    logging.debug(' pppoe_ip=' + str(pppoe_ip) + '\n' +
                  ' pppoe_pw=' + str(pppoe_pw) + '\n' +
                  ' pppoe_user=' + str(pppoe_user) + '\n' +
                  ' pppoe_pwd=' + str(pppoe_pwd))
    script_page.open_url(driver, 'http://' + pppoe_ip)
    script_page.login(driver, pppoe_pw)
    if script_page.connect_pppoe(driver, pppoe_user, pppoe_pwd) == 1:
        logging.info('test pppoe connect success')
    else:
        logging.warning('test pppoe connect fail!!!')


def mac_clone(driver, config_parser):
    logging.info('D1_mac_clone 在页面点击克隆MAC地址，重进页面后查看当前mac')
    default_ip = config_parser.get('Default', 'default_ip')
    default_pw = config_parser.get('Default', 'default_pw')
    script_page.open_url(driver, 'http://' + default_ip)
    script_page.login(driver, default_pw)
    cur_mac = script_page.clone_cur_mac(driver)
    script_page.open_url(driver, 'http://' + default_ip)
    script_page.login(driver, default_pw)
    try:
        logging.debug('点击mac克隆页面')
        driver.find_element_by_css_selector('#clonemac > span').click()
        time.sleep(5)
        logging.debug('获取当前mac地址')
        new_mac = driver.find_element_by_css_selector("input.clone_cur_inputmac").get_attribute("value")
        if cur_mac == new_mac:
            logging.info('test mac clone success')
        else:
            logging.warning('test mac clone fail!!!')
    except Exception as e:
        logging.debug(e)


'''
    a = []
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
'''


def file_view(driver, config_parser):
    logging.info('D1_file_view 遍历映射盘符下所有文件夹和文件与页面上 文件查看 结果对比')
    Test_file_view.file_view_folders(driver, config_parser)
    Test_file_view.file_view_files(driver, config_parser)


def set_ssid(driver, config_parser):
    logging.info('D1_set_ssid， 修改2.4G和5G的ssid')
    ssid_ip = config_parser.get('SSID', 'ssid_ip')
    ssid_pw = config_parser.get('SSID', 'ssid_pw')
    ssid24 = (config_parser.get('SSID', 'ssid24')).split(',')
    ssid5 = (config_parser.get('SSID', 'ssid5')).split(',')
    id24 = 'wifinfo_24'
    id5 = 'wifinfo_5'
    logging.debug(' test_ip=' + str(ssid_ip) + '\n' +
                  ' test_pw=' + str(ssid_pw) + '\n' +
                  ' ssid24=' + str(ssid24) + '\n' +
                  ' ssid5=' + str(ssid5)
                  )

    def input_ssid(css_id, ssid):
        logging.debug(ssid)
        script_page.open_url(driver, 'http://' + ssid_ip)
        script_page.login(driver, ssid_pw)
        a = ''
        try:
            driver.find_element_by_id(css_id).click()
            time.sleep(5)
            driver.find_element_by_css_selector("input.netssid.setwireturn_input").clear()
            driver.find_element_by_css_selector("input.netssid.setwireturn_input").send_keys(ssid)
            time.sleep(1)
            driver.find_element_by_css_selector("a.subbtn.saveStatus > b").click()
            time.sleep(10)
            script_page.open_url(driver, 'http://' + ssid_ip)
            script_page.login(driver, ssid_pw)
            driver.find_element_by_id(css_id).click()
            time.sleep(5)
            a = driver.find_element_by_css_selector("input.netssid.setwireturn_input").get_attribute("value")
        except Exception as e:
            logging.info(e)
        if ssid == a:
            logging.info('test set ssid success')
        else:
            logging.warning('test set ssid fail!!!')
            logging.debug(a)
            logging.debug(ssid)

    for ss in ssid24:
        input_ssid(id24, ss)
    for ss in ssid5:
        input_ssid(id5, ss)


def new_password(driver, config_parser):
    logging.info('D1_new_password 修改管理员密码，重新登录算成功')

    pass_ip = config_parser.get('Password', 'pass_ip')
    pass_pw = [config_parser.get('Password', 'pass_pw')]
    password = (config_parser.get('Password', 'password')).split(',')
    ppp = pass_pw + password

    logging.debug(' pass_ip=' + str(pass_ip) + '\n' +
                  ' pass_pw=' + str(pass_pw) + '\n' +
                  ' password=' + str(password)
                  )

    def setpasswd(old_passwd, new_passwd):
        try:
            script_page.open_url(driver, 'http://' + pass_ip)
            script_page.login(driver, old_passwd)
            logging.debug('进入密码修改页面')
            driver.find_element_by_id('setpasswd').click()
            time.sleep(5)
            logging.debug('输入旧密码')
            driver.find_element_by_id("oldPasswd").clear()
            driver.find_element_by_id("oldPasswd").send_keys(old_passwd)
            logging.debug('输入新密码')
            driver.find_element_by_id("newPasswd").clear()
            driver.find_element_by_id("newPasswd").send_keys(new_passwd)
            driver.find_element_by_id("renewPasswd").clear()
            driver.find_element_by_id("renewPasswd").send_keys(new_passwd)
            logging.debug('点击确定')
            driver.find_element_by_id("setNewPasswd").click()
            time.sleep(10)
            script_page.open_url(driver, 'http://' + pass_ip)
            script_page.login(driver, new_passwd)
            return 1
        except Exception as e:
            logging.error(e)
            return 0

    for i in range(len(ppp) - 1):
        logging.debug('旧密码=' + str(ppp[i]))
        logging.debug('新密码=' + str(ppp[i + 1]))
        if setpasswd(ppp[i], ppp[i + 1]) == 1:
            logging.info('test set password success new_pwd=' + str(ppp[i + 1]))
        else:
            logging.warning('test set password fail!!!')
    if setpasswd(ppp[-1], ppp[0]) == 1:
        logging.info('recover password success new_pwd=' + str(ppp[0]))
    else:
        logging.warning('recover password fail!!!')


def qos(driver, config_parser):
    logging.info('D1_QOS ')
    qos_ip = config_parser.get('Qos', 'qos_ip')
    qos_pw = config_parser.get('Qos', 'qos_pw')
    down_limit = config_parser.get('Qos', 'down_limit')
    up_limit = config_parser.get('Qos', 'up_limit')
    down_url = config_parser.get('Qos', 'down_url')
    up_url = config_parser.get('Qos', 'up_url')
    up_file = config_parser.get('Qos', 'up_file')
    data = {'file': open(up_file, 'rb')}

    logging.debug(' qos_ip=' + str(qos_ip) + '\n' +
                  ' qos_pw=' + str(qos_pw) + '\n' +
                  ' down_limit=' + str(down_limit) + '\n' +
                  ' up_limit=' + str(up_limit) + '\n' +
                  ' down_url=' + str(down_url) +'\n' +
                  ' up_url=' + str(up_url) + '\n' +
                  ' up_file=' + str(up_file)
                  )

    def qosturn(down, up):
        try:
            script_page.open_url(driver, 'http://' + qos_ip)
            script_page.login(driver, qos_pw)
            logging.debug('进入QOS页面')
            driver.find_element_by_id('qosselect').click()
            time.sleep(5)
            logging.debug('打开QOS开关')
            driver.find_element_by_css_selector("input.qosturn").click()
            time.sleep(1)
            logging.debug('输入下载，上传速度')
            driver.find_element_by_css_selector("input.qosipstore.downkbps").clear()
            time.sleep(1)
            driver.find_element_by_css_selector("input.qosipstore.downkbps").send_keys(down)
            time.sleep(1)
            driver.find_element_by_css_selector("input.qosipstore.upkbps").clear()
            time.sleep(1)
            driver.find_element_by_css_selector("input.qosipstore.upkbps").send_keys(up)
            time.sleep(1)
            logging.debug('点击保存')
            driver.find_element_by_css_selector("a.subbtn.save_smartqosnet > b").click()
            time.sleep(20)
            return 1
        except Exception as e:
            logging.debug(e)
            return 0

    def download(url):
        url = url.strip()
        try:
            s = time.time()
            result = urllib.request.urlretrieve(url, 'temp', )
            e = time.time()
            down_time = e - s
            headers = result[1]
            if 'Content-Length' in headers:
                file_size = int(headers['Content-Length'])
            else:
                file_size = 0
            return {'result': 'success', 'size': file_size, 'time': down_time}
        except Exception as e:
            return {'result': e, 'size': 0, 'time': 0}

    def upload(url, file):
        try:
            s = time.time()
            result = requests.post(url, files=data)
            e = time.time()
            up_time = e - s
            if '200' in str(result):
                return up_time
            else:
                return -1
        except Exception as e:
            logging.debug(e)
            return -1

    if qosturn(down_limit, up_limit) == 1:
        down_res = download(down_url)
        if down_res.get('result') == 'success':
            size = round(down_res.get('size') / 1024, 2)
            t = round(down_res.get('time'), 2)
            down_speed = round(size / t, 2)
            print(down_speed)
            print(int(down_limit) * 1024 / 8)
            if int(down_speed) < int(down_limit) * 1024 / 8:
                logging.info('test download limit success')
            else:
                logging.warning('test download limit fail!!!')
        size = os.path.getsize(up_file)/1024
        up_res = upload(up_url, up_file)
        print(up_res)
        if up_res > 0:
            up_speed = size/up_res
            print(up_speed)
            if int(up_speed) < int(up_limit) * 1024 / 8:
                logging.info('test up limit success')
            else:
                logging.warning('test up limit fail!!!')
