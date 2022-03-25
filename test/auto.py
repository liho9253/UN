# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
path = r"C:/Program Files/python/chromedriver.exe"
driver = webdriver.Chrome(path)

def Task():
    f = open('shitwait.txt', 'r', encoding='UTF-8')
    msg = []
    
    for line in f:
        s = line.split(",")
        for i in range(0,len(s)):
            msg.append(s[i])
    print(len(msg))
    print(msg[105])
    driver.get("http://yibian.hopto.org/acu/")
    # search = driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
    # search.clear()
    # search.send_keys("天府穴" + "再探針灸大成")
    # search.send_keys(Keys.RETURN)
    time.sleep(2)
    
    # for i in range(0,1):
    #     ch = driver.find_elements_by_class_name("LC20lb")[i]
    #     ch.click()
    #     time.sleep(2)
        
    #     driver.back()
    #     time.sleep(2)
        
    f.close()
        
Task()

driver.quit()

