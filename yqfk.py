#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
import requests
import logging
import signal

username = 'your student number'
password = 'your password'
# 可选
sckey = ''
payload = {'text': u'今日提交成功', 'desp': ''}
# logging
logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s:%(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

# fail-fast
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--no-proxy-server')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#disable proxy in headless mode
chrome_options.add_argument('--proxy-server="direct://"')
chrome_options.add_argument('--proxy-bypass-list=*')
driver = webdriver.Chrome(options=chrome_options)

def exit_handler(signum, frame):
    driver.quit()
    exit()

signal.signal(signal.SIGTERM, exit_handler)
signal.signal(signal.SIGINT, exit_handler)

def submit_form():

    # login
    logger.info(u'登录中')
    driver.get('https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html')
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('casPassword').send_keys(password)
    driver.find_element_by_id('loginBtn').click()

    # wait redirect
    wait = WebDriverWait(driver, 90)
    wait.until(EC.url_contains('yqfk.dgut.edu.cn/main'))
    logger.info(u'登录成功')

    # 等代身份信息加载，可能是已经打卡，也可能还没打卡 
    wait.until(lambda driver: u"打卡" in driver.page_source)

    retry_times = 0
    # 您今日尚未打卡
    while u"提交成功" not in driver.page_source and retry_times < 3:
        logger.info(u'尝试提交')
        retry_times += 1
        # 要等待多个 ajax 请求
        time.sleep(5 * retry_times)
        # submit
        if driver.find_elements_by_css_selector('.am-button.am-button-primary'):
            logger.info(u'点击提交')
            driver.find_element_by_css_selector('.am-button.am-button-primary').click()
            time.sleep(5 * retry_times)

    # 没有提交成功等一个小时后再运行一次
    if u"提交成功" not in driver.page_source:
        logger.info(u'提交失败，等待重新提交')
        run_date = datetime.now() + timedelta(hours=1)
        scheduler.add_job(submit_form, 'date', run_date=run_date)
    else:
        # 提交成功
        # 如果配置了 sckey 就推送消息到微信
        logger.info(u'提交成功')
        if sckey:
            requests.post('https://sc.ftqq.com/' + sckey + '.send', data=payload)
            logger.info(u'发送推送')


scheduler = BlockingScheduler({'apschedule.timezone': 'Asia/Shanghai'})
# 每天晚上 12:30 运行
scheduler.add_job(submit_form, 'cron', hour=0, minute=30)
# fail-fast
submit_form()
scheduler.start()
