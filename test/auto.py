# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException
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
    driver.get("http://yibian.hopto.org/acu/")
    for i in range(1,8):
        for j in range(1,3):
            t1 = driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td[1]/table/tbody/tr["+str(i)+"]/td["+str(j)+"]/a")
            t1.click()
            time.sleep(1)
            with open('information.txt', 'a', encoding='UTF-8') as f2:
                for k in range(1,35):
                    for z in range(1,3):
                        try:
                            t2 = driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td[3]/table/tbody/tr["+str(k)+"]/td["+str(z)+"]/a")
                            t2.click()
                            time.sleep(2)
                            # f2.write(driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/table[1]/tbody/tr[1]/td[2]/b").text+",")
                            print(driver.find_elements_by_link_text("釋名").findNext('p').text)
                        except NoSuchElementException:
                            break
                        driver.back()
            time.sleep(1)
    time.sleep(2)
    # for i in range(0,1):
    #     ch = driver.find_elements_by_class_name("LC20lb")[i]
    #     ch.click()
    #     time.sleep(2)
        
    #     driver.back()
    #     time.sleep(2)
    f2.close()
    f.close()
        
Task()

driver.quit()

