# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
path = r"C:/Program Files/python/chromedriver.exe"
driver = webdriver.Chrome(path)
def Task():
    # f = open('shitwait.txt', 'r', encoding='UTF-8')
    
    
    # msg = []
    # for line in f:
    #     s = line.split(",")
    #     for i in range(0,len(s)):
    #         msg.append(s[i])
    driver.get("http://yibian.hopto.org/acu/")
    for i in range(1,3):
        for j in range(1,3):
            t1 = driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td[1]/table/tbody/tr["+str(i)+"]/td["+str(j)+"]/a")
            t1.click()
            with open('information.txt', 'a', encoding='UTF-8') as f2:
                for k in range(1,40):
                    for z in range(1,3):
                        try:
                            # t2 = driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td[3]/table/tbody/tr["+str(k)+"]/td["+str(z)+"]/a")
                            # t2.click()
                            # WebDriverWait(driver, 10).until(
                            #     EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/table[2]/tbody/tr/td/font[1]"))
                            #     )
                            driver.back()
                            # print(driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/table[1]/tbody/tr[1]/td[2]/b").text)
                            # name_s = driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/table[1]/tbody/tr[1]/td[2]/b").text
                            # f2.write(name_s+"\n")
                            # p = driver.find_elements_by_tag_name("p")
                            # for p_l in p:
                            #     if p_l.text == "":
                            #         break
                            #     else:
                            #         f2.write(p_l.text+"\n")
                            # ul = driver.find_elements_by_tag_name("ul")
                            # for ul_l in ul:
                            #     f2.write(ul_l.text+"\n")
                        except NoSuchElementException:
                            break
                        
                        
            time.sleep(1)
    time.sleep(2)
    f2.close()
    # f.close()
        
Task()

driver.quit()

