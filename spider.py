# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import html5lib
from numpy import NaN
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
desired_capabilities = DesiredCapabilities.FIREFOX # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "eager" # 页面加载模式:把所有组件都加载全

import json as js
dict_key = {}

def realtime_data(location):
    if(location not in dict_key.keys()):
        url = r'http://www.src.weather.com.cn/'
        browser = webdriver.Firefox()
        browser.set_page_load_timeout(10)
        try:
            browser.get(url)
        except:
            browser.execute_script("window.stop()")
        browser.implicitly_wait(10)
        browser.find_element(by=By.ID,value='txtZip').send_keys(location)
        browser.implicitly_wait(10)
        key = browser.find_element(by=By.XPATH,value=
            '//li//b[contains(text(),\'{}\')]/..'.format(location)).get_attribute('num') #get city`s id
        dict_key[location] = key
    else:
        key = dict_key[location]
        browser = webdriver.Firefox()
        browser.set_page_load_timeout(10)
    url = 'http://www.src.weather.com.cn/weather1d/{}.shtml'.format(key)
    flag = True
    while flag:
        try:
            browser.get(url)
            browser.implicitly_wait(1000)
            elements = browser.find_element(by=By.XPATH,value=
                '''//div[@class='t']''').text.split('\n')
            offset = 0
            if(elements[1]!='相对湿度'): #可能有多一行'暴雨预警'的情况,此时需要特殊判定
                offset = 1
                elements[1] = elements[0]+elements[1]
            ans = {'time':elements[offset],'wet':elements[2+offset],'wind':elements[3+offset],'wind_level':elements[4+offset],
                'celsius':elements[5+offset],'air_level':eval(elements[6+offset][:-1])}
            flag = False
        except:
            flag = True
    browser.quit()
    return ans

def parse_urlpage(location):
    url = r'http://www.src.weather.com.cn/'
    browser = webdriver.Firefox()
    browser.set_page_load_timeout(10)
    try:
        browser.get(url)
    except:
        browser.execute_script("window.stop()")
    browser.implicitly_wait(10)
    browser.find_element(by=By.ID,value='txtZip').send_keys(location)
    browser.implicitly_wait(10)
    key = browser.find_element(by=By.XPATH,value=
        '//li//b[contains(text(),\'{}\')]/..'.format(location)).get_attribute('num') #get city`s id
    ##40days
    data_40d = {'TIME':[],'CELSIUS1':[],'CELSIUS2':[]}
    url = 'http://www.src.weather.com.cn/weather40d/{}.shtml'.format(key)
    browser.set_page_load_timeout(10)
    try:
        browser.get(url)
    except:
        browser.execute_script("window.stop()")
    browser.implicitly_wait(5)
    cnt=0
    while cnt<47:
        elements = browser.find_elements(by=By.XPATH,value=
        '''//table/tbody/tr/td[starts-with(@class,'d')]''')
        cnt+= len(elements)
        for element in elements:
            q = element.text.split('\n')
            if(len(q)<5):
                continue
            data_40d['TIME'].append(q[1])
            data_40d['CELSIUS1'].append(eval(q[4][:-1]))
            data_40d['CELSIUS2'].append(eval(q[3][:-1]))
        if(cnt<47):
            button = browser.find_element(by=By.XPATH,value = '''//span[contains(@class,'Y_right right_rili')]''')
            button.click() #翻页
    ###1day
    url = 'http://www.src.weather.com.cn/weather1d/{}.shtml'.format(key)
    try:
        browser.get(url)
    except:
        browser.execute_script("window.stop()")
    browser.implicitly_wait(1000)
    try:
        elements = browser.find_element(by=By.XPATH,value=
         '''//div[@class='t']''').text.split('\n')
        air_level = eval(elements[6][:-1])
    except:
        air_level = 'undefined'
    browser.quit()
    ###7days
    r = requests.get('http://www.src.weather.com.cn/weather/{}.shtml'.format(key))
    text = r.content.decode('utf-8')
    soup = BeautifulSoup(text, 'html5lib')
    di = soup.find('div', class_='c7d')
    scr = di.find('script')
    raw = js.loads(scr.contents[0].split('=')[1])['7d']
    data_7d = {'TIME':[],'WEATHER':[],'CELSIUS':[],'WIND':[],'WIND_LEVEL':[],'BLUE':[]}
    for i in raw:
        for j in i:
            q = j.split(',')
            data_7d['TIME'].append(q[0])
            data_7d['WEATHER'].append(q[2])
            data_7d['CELSIUS'].append(eval(q[3][:-1]))
            data_7d['WIND'].append(q[4])
            data_7d['WIND_LEVEL'].append(q[5])
            data_7d['BLUE'].append(q[6])
    dict_key[location] = key
    return {'air_level':air_level,'data_7d':data_7d,'data_40d':data_40d}

if __name__ == '__main__':
    locs = ['孝感']
    for i in locs:
        realtime_data(i)