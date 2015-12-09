# -*- coding:utf-8 -*-

import time
import logging
from selenium.webdriver.support.ui import Select


def open_url(driver, url):
    time.sleep(1)
    try:
        logging.info("try open " + url)
        driver.get(url)
        return 1
    except Exception as e:
        logging.warning("===open url=== %s", e)
        return 0


def detect_wan(driver):
    flag = ['运营商', 'DHCP']
    try:
        tip = str(driver.find_element_by_css_selector("p.tips-text").text)
        for a in flag:
            if tip.find(a) > -1:
                return a
    except Exception as e:
        print(e)
        return 0


def initialize(driver, url, password, usr='', pw=''):
    try:
        time.sleep(3)
        driver.get(url)
        time.sleep(3)
        driver.find_element_by_id("init-protocol-checkbox").click()
        time.sleep(3)
        driver.find_element_by_id("initalize").click()
        time.sleep(30)
        wan = detect_wan(driver)
        if wan == 0:
            logging.info('wan = 跳过检测')
            driver.find_element_by_link_text(u"跳过检测").click()
        else:
            if 'DHCP' == wan:
                logging.info('wan = '+wan)
                driver.find_element_by_link_text(u"下一步").click()
                time.sleep(10)
            if '运营商' == wan:
                logging.info('wan = '+wan)
                #TODO
        time.sleep(3)
        driver.find_element_by_id("key").clear()
        time.sleep(3)
        driver.find_element_by_id("key").send_keys(password)
        time.sleep(3)
        driver.find_element_by_id("wifi").click()
        time.sleep(5)
        driver.find_element_by_link_text(u"登录路由器").click()
        return 1
    except Exception as e:
        logging.warning("===init=== %s", e)
        return 0


def login(driver, password):
    time.sleep(1)
    try:
        logging.info("try login password = " + password)
        driver.find_element_by_id("focus_password").clear()
        driver.find_element_by_id("focus_password").send_keys(password)
        driver.find_element_by_css_selector("img.login_form_img").click()
        time.sleep(5)
        if driver.find_element_by_css_selector("a.logo"):
            return 1
    except Exception as e:
        logging.warning("===init=== %s", e)
        return 0


def login_y1(driver, password):
    time.sleep(1)
    try:
        logging.info("try login password = " + password)
        driver.find_element_by_id("focus_password").clear()
        driver.find_element_by_id("focus_password").send_keys(password)
        driver.find_element_by_css_selector("img.login_form_img").click()
        time.sleep(2)
        driver.find_element_by_id("popup-qrcode-close").click()
        time.sleep(2)
        if driver.find_element_by_css_selector("a.logo"):
            return 1
    except Exception as e:
        logging.warning("===login=== %s", e)
        return 1


def set_5ssid(driver, value):
    time.sleep(1)
    try:
        logging.info("try set 5G ssid = " + value)
        driver.find_element_by_id("wifinfo_5").click()
        time.sleep(5)
        driver.find_element_by_css_selector("input.netssid.setwireturn_input").clear()
        time.sleep(1)
        driver.find_element_by_css_selector("input.netssid.setwireturn_input").send_keys(value)
        time.sleep(1)
        driver.find_element_by_css_selector("a.subbtn.saveStatus > b").click()
        time.sleep(16)
        driver.find_element_by_css_selector("a.setup_return").click()
        time.sleep(3)
        return 1
    except Exception as e:
        logging.warning("===set 5G ssid=== %s ", e)
        return 0


def set_24ssid(driver, value):
    time.sleep(1)
    try:
        logging.info("try set 2.4G ssid = " + value)
        driver.find_element_by_id("wifinfo_24").click()
        time.sleep(5)
        driver.find_element_by_css_selector("input.netssid.setwireturn_input").clear()
        time.sleep(1)
        driver.find_element_by_css_selector("input.netssid.setwireturn_input").send_keys(value)
        time.sleep(1)
        driver.find_element_by_css_selector("a.subbtn.saveStatus > b").click()
        time.sleep(16)
        driver.find_element_by_css_selector("a.setup_return").click()
        time.sleep(3)
        return 1
    except Exception as e:
        logging.warning("===set 5G ssid=== %s ", e)
        return 0


def get_5ssid(driver):
    time.sleep(1)
    try:
        logging.info("try get 5G ssid...")
        driver.find_element_by_id("wifinfo_5").click()
        time.sleep(5)
        return driver.find_element_by_css_selector("input.netssid.setwireturn_input").get_attribute("value")
    except Exception as e:
        logging.warning("===get ssid=== %s", e)
        return None


def get_24ssid(driver):
    time.sleep(1)
    try:
        logging.info("try get 2.4G ssid...")
        driver.find_element_by_id("wifinfo_24").click()
        time.sleep(5)
        return driver.find_element_by_css_selector("input.netssid.setwireturn_input").get_attribute("value")
    except Exception as e:
        logging.warning("===get ssid=== %s", e)
        return None


def reset(driver, wait_time):
    time.sleep(1)
    try:
        logging.info("try reset...")
        driver.find_element_by_id("flashops").click()
        time.sleep(2)
        driver.find_element_by_id("reset").click()
        time.sleep(2)
        driver.find_element_by_id("reset_btn").click()
        time.sleep(3)
        driver.find_element_by_css_selector(
            "div.tcontent > div.reset_correct > div.reset_pop_surebox > a.subbtn.surereset > b").click()
        time.sleep(2)
        logging.info('now Reseting wait %s', wait_time)
        time.sleep(wait_time)
        return 1
    except Exception as e:
        logging.warning("===reset=== %s", e)
        return 0


def restart(driver, wait_time):
    time.sleep(1)
    try:
        logging.info("try restart...")
        driver.find_element_by_id("restart").click()
        time.sleep(2)
        driver.find_element_by_css_selector("a.subbtn1.restart_btn > b").click()
        time.sleep(8)
        driver.find_element_by_css_selector(
            "div.tcontent > div.restart_correct > div.restart_pop_surebox > a.subbtn.surerestart > b").click()
        time.sleep(1)
        logging.info('now Restarting wait %s', wait_time)
        time.sleep(wait_time)
        return 1
    except Exception as e:
        logging.warning("===restart=== %s", e)
        return 0


def upgrade(driver, build, wait_time):
    try:
        logging.info("try upgrade to " + build)
        driver.find_element_by_link_text(u"固件升级").click()
        time.sleep(5)
        driver.find_element_by_id("firmware_file").send_keys(build)
        time.sleep(5)
        driver.find_element_by_class_name("firmwarebtn").click()
        time.sleep(15)
        logging.info('now upgrading wait %s', wait_time)
        time.sleep(wait_time)
        return 1
    except Exception as e:
        logging.warning("===upgrade=== %s", e)
        return 0


def get_version(driver):
    try:
        logging.info("try get version...")
        return driver.find_element_by_xpath("//div[@id='left_nav']/div[2]/div[2]/p[2]/span[2]").text
    except Exception as e:
        logging.warning("===get version=== %s", e)
        return None


def connect_pppoe(driver, pst, pwd):
    try:
        logging.info("try connect pppoe...")
        driver.find_element_by_id("wifi").click()
        time.sleep(2)
        Select(driver.find_element_by_css_selector("select.wanchange")).select_by_visible_text(u"PPPoE拨号")
        time.sleep(2)
        driver.find_element_by_css_selector("input.wify_long.pppoe_pst").clear()
        driver.find_element_by_css_selector("input.wify_long.pppoe_pst").send_keys(pst)
        driver.find_element_by_css_selector("input.wify_long.pppoe_pwd").clear()
        driver.find_element_by_css_selector("input.wify_long.pppoe_pwd").send_keys(pwd)
        driver.find_element_by_css_selector("a.dial > b").click()
        time.sleep(30)
        if driver.find_element_by_xpath("//span[@id='pppoe_btn']/a/b"):
            return 1
        else:
            return 0
    except Exception as e:
        logging.warning(e)
        return 0


def disconnect_pppoe(driver):
    try:
        logging.info("try disconnect pppoe...")
        driver.find_element_by_id("wifi").click()
        time.sleep(2)
        driver.find_element_by_xpath("//span[@id='pppoe_btn']/a/b").click()
        time.sleep(10)
        if driver.find_element_by_css_selector("a.dial > b"):
            return 1
        else:
            return 0
    except Exception as e:
        logging.warning(e)
        return 0


def clone_cur_mac(driver):
    try:
        logging.info("try clone_cur_mac...")
        driver.find_element_by_css_selector('#clonemac > span').click()
        time.sleep(3)
        cur_mac = driver.find_element_by_css_selector("span.clone_cur_mac").text
        driver.find_element_by_link_text(u"克隆MAC地址").click()
        time.sleep(1)
        driver.find_element_by_css_selector("a.subbtn.macsave > b").click()
        time.sleep(10)
        return cur_mac
    except Exception as e:
        logging.warning(e)
        return 0