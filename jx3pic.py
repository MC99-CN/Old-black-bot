# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 14:03:27 2022

@author: Administrator
"""

import requests
import json
import random
from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By


def jx3_pic():
    url = 'https://origin.jx3box.com/emotion/'
    url = url + str(random.randint(1, 983))
    return url

def get_jx3_url():

    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 设置option
    driver = webdriver.Chrome(chrome_options=option)  # 调用带参数的谷歌浏览器
    driver.get(jx3_pic())
    driver.maximize_window()
    time.sleep(0.5)
    pic = driver.find_element_by_xpath('//*[@id="app"]/main/div/div/div[1]/div[2]/div[1]/a/img')
    img_list0 = pic.get_attribute('src')
    time.sleep(0.5)
    driver.quit()
    return img_list0