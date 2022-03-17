from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = r"C:/Program Files/python/chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get("https://www.acc.com.tw/investor-realtions/financial-information")

# search = {'k': "亞泥 銷售資料"}

    
d1 = driver.find_element_by_id("revenue").find_element_by_class_name("table-container")
d2 = d1.find_element_by_tag_name("table").find_element_by_tag_name("thead").find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("th")
with open("text.txt", "a") as f:
    for i in d2:
        f.write(i.text)
        f.write("\n")
driver.quit()