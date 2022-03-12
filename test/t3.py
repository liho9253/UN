from selenium import webdriver
import time



path = r"C:/Program Files/python/chromedriver.exe"
driver = webdriver.Chrome(path)

time.sleep(1)
driver.get("https://www.acc.com.tw/investor-realtions/financial-information")

tables = driver.find_element_by_xpath("//*[@id='revenue']/div/table/tbody")
# for tr in lists:
tables_tr = tables.find_element_by_xpath("//*[@id='revenue']/div/table/tbody/tr")
print(tables_tr[0].text)
time.sleep(1)
driver.quit()