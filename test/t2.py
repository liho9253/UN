from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:/Program Files/python/chromedriver.exe"
driver = webdriver.Chrome(PATH)


driver.get("https://www.acc.com.tw/investor-realtions/financial-information")

year = driver.find_element_by_id("year")
year.click()

year_2015 = driver.find_element_by_xpath("//*[@id='year']/option[8]")
year_2015.click()

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "66,435,527"))
)
number = driver.find_elements_by_class_name("number")

with open('text.txt', "a") as f:
    for num in number:
        f.write(num.text)
        f.write('\n')
        
        
    

time.sleep(2)
driver.quit()

