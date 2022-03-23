# -*- coding: UTF-8 -*-
from selenium import webdriver

path = r"C:/Program Files/python/chromedriver.exe"
driver = webdriver.Chrome(path)

def d1():
    driver.get("https://acupun.site/FourteenChannel/LU_S.html")
    ap_1 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_1 = driver.find_elements_by_tag_name("tr")
    with open ('手太陰肺經穴.txt', 'w', encoding='UTF-8') as f:
        for i in range(1, 12):
            if i == 11:
                f.write(ap_1[i].find_elements_by_tag_name("td")[0].text)
            else:
                f.write(ap_1[i].find_elements_by_tag_name("td")[0].text+",")
                
def d2():
    driver.get("https://acupun.site/fourteenchannel/si.html")
    ap_2 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_2 = driver.find_elements_by_tag_name("tr")
    with open('手太陽小腸經.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,20):
            if i == 19:
                f.write(ap_2[i].find_elements_by_tag_name("td")[0].text)
            else:
                f.write(ap_2[i].find_elements_by_tag_name("td")[0].text+",")
            
def d3():
    driver.get("https://acupun.site/fourteenchannel/st.html")
    ap_3 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_3 = driver.find_elements_by_tag_name("tr")
    with open('足陽明胃經穴位圖.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,46):
            if i == 45:
                f.write(ap_3[i].find_elements_by_tag_name("td")[0].text)
            else:
                f.write(ap_3[i].find_elements_by_tag_name("td")[0].text+",")
def d4():
    driver.get("https://acupun.site/FourteenChannel/DU.html")
    ap_4 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_4 = driver.find_elements_by_tag_name("tr")
    with open('督脈穴位圖.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,29):
            if i == 28:
                f.write(ap_4[i].find_elements_by_tag_name("td")[0].text)
            else:
                f.write(ap_4[i].find_elements_by_tag_name("td")[0].text+",")

    
if __name__ == '__main__':
    d1()
    d2()
    d3()
    d4()
    
driver.quit()