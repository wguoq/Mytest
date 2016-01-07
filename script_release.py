import time
import script_page
import Test_file_view
import logging


def init_config(driver, configparser):
    logging.info('D1_initialize 不插网线/DHCP/拨号都支持，完成配置进入首页算成功')
    default_ip = configparser.get('Default', 'default_ip')
    default_pw = configparser.get('Default', 'default_pw')
    pppoe_user = configparser.get('PPPOE', 'pppoe_user')
    pppoe_pwd = configparser.get('PPPOE', 'pppoe_pwd')
    logging.debug(' default_ip=' + str(default_ip) +
                  ' default_pw=' + str(default_pw) +
                  ' pppoe_user=' + str(pppoe_user) +
                  ' pppoe_pwd=' + str(pppoe_pwd)
                  )
    if script_page.initialize(driver, 'http://' + default_ip, default_pw, pppoe_user, pppoe_pwd) == 1:
        logging.info('init_config success')
    else:
        logging.warning('init_config fail!!!')


def login(driver, configparser):
    logging.info('D1_login 输入密码，进入首页算成功')
    default_ip = configparser.get('Default', 'default_ip')
    default_pw = configparser.get('Default', 'default_pw')
    logging.debug(' default_ip=' + str(default_ip) +
                  ' default_pw=' + str(default_pw))
    script_page.open_url(driver, 'http://' + default_ip)
    if script_page.login(driver, default_pw) == 1:
        logging.info('login success')
    else:
        logging.warning('login fail!!!')


def pppoe(driver, configparser):
    logging.info('D1_pppoe 输入账号密码拨号，页面返回连接成功就算成功，不验证是否上网')
    pppoe_ip = configparser.get('PPPOE', 'pppoe_ip')
    pppoe_pw = configparser.get('PPPOE', 'pppoe_pw')
    pppoe_user = configparser.get('Default', 'pppoe_user')
    pppoe_pwd = configparser.get('Default', 'pppoe_pwd')
    script_page.open_url(driver, 'http://' + pppoe_ip)
    script_page.login(driver, pppoe_pw)
    if script_page.connect_pppoe(driver, pppoe_user, pppoe_pwd) == 1:
        logging.info('pppoe connect success')
    else:
        logging.warning('pppoe connect fail!!!')


def mac_clone(driver, configparser):
    logging.info('D1_mac_clone ')
    default_ip = configparser.get('Default', 'default_ip')
    default_pw = configparser.get('Default', 'default_pw')
    script_page.open_url(driver, 'http://' + default_ip)
    script_page.login(driver, default_pw)
    cur_mac = script_page.clone_cur_mac(driver)
    script_page.open_url(driver, 'http://' + default_ip)
    script_page.login(driver, default_pw)
    driver.find_element_by_css_selector('#clonemac > span').click()
    time.sleep(5)
    new_mac = driver.find_element_by_css_selector("input.clone_cur_inputmac").get_attribute("value")
    if cur_mac == new_mac:
        logging.info('mac clone success')
    else:
        logging.warning('mac clone fail!!!')


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


def file_view(driver, configparser):
    Test_file_view.file_view_folders(driver, configparser, logging)
    Test_file_view.file_view_files(driver, configparser, logging)


def set_ssid(driver, configparser):
    logging.info('2.4ssid')
    test_ip = configparser.get('Release', 'test_ip')
    test_pw = configparser.get('Release', 'test_pw')
    ssid24 = (configparser.get('Release', 'ssid24')).split(',')
    ssid5 = (configparser.get('Release', 'ssid5')).split(',')
    id24 = 'wifinfo_24'
    id5 = 'wifinfo_5'

    def aaa(css_id, ssid):
        logging.info(ssid)
        script_page.open_url(driver, 'http://' + test_ip)
        script_page.login(driver, test_pw)
        a = ''
        try:
            driver.find_element_by_id(css_id).click()
            time.sleep(5)
            driver.find_element_by_css_selector("input.netssid.setwireturn_input").clear()
            driver.find_element_by_css_selector("input.netssid.setwireturn_input").send_keys(ssid)
            time.sleep(1)
            driver.find_element_by_css_selector("a.subbtn.saveStatus > b").click()
            time.sleep(10)
            script_page.open_url(driver, 'http://' + test_ip)
            script_page.login(driver, test_pw)
            driver.find_element_by_id(css_id).click()
            time.sleep(5)
            a = driver.find_element_by_css_selector("input.netssid.setwireturn_input").get_attribute("value")
        except Exception as e:
            logging.info(e)
        if ssid == a:
            logging.info('set ssid success')
        else:
            logging.warning('set ssid fail!!!')
            logging.debug(a)
            logging.debug(ssid)
    for ss in ssid24:
        aaa(id24, ss)
    for ss in ssid5:
        aaa(id5, ss)


def new_password():
    print('D1_new_password')
