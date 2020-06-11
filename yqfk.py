#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta

username = 'your student number'
password = 'your password'

# fail-fast
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)

def submit_form():

    # login
    driver.get('https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html')
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('casPassword').send_keys(password)
    driver.find_element_by_id('loginBtn').click()

    # wait redirect
    wait = WebDriverWait(driver, 90)
    wait.until(EC.url_contains('yqfk.dgut.edu.cn/main'))

    # 等代身份信息加载，可能是已经打卡，也可能还没打卡 
    wait.until(lambda driver: "打卡" in driver.page_source)

    retry_times = 0
    # 您今日尚未打卡
    while "提交成功" not in driver.page_source and retry_times < 3:
        retry_times += 1
        # 要等待多个 ajax 请求
        time.sleep(5 * retry_times)
        # submit
        driver.find_element_by_css_selector('.am-button.am-button-primary').click()

    # 没有提交成功等一个小时后再运行一次
    if "提交成功" not in driver.page_source:
        run_date = datetime.now() + timedelta(hours=1)
        scheduler.add_job(submit_form, 'date', run_date=run_date)

scheduler = BlockingScheduler({'apschedule.timezone': 'Asia/Shanghai'})
# 每天 12:30 运行
scheduler.add_job(submit_form, 'cron', hour=12, minute=30)
scheduler.start()
