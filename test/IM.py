# -*- coding: UTF-8 -*-
from selenium import webdriver

path = r"C:/Program Files/python/chromedriver.exe"
driver = webdriver.Chrome(path)

def d1():
    driver.get("https://acupun.site/FourteenChannel/LU.html")
    ap_1= driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_1 = driver.find_elements_by_tag_name("tr")
    with open ('one.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,13):
            if i == 12:
                f.write(ap_1[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_1[i].find_elements_by_tag_name("td")[j].text+","+"\n")
                    
                

def d2():
    driver.get("https://acupun.site/fourteenchannel/si.html")
    ap_2 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_2 = driver.find_elements_by_tag_name("tr")
    with open ('two.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,21):
            if i == 20:
                f.write(ap_2[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_2[i].find_elements_by_tag_name("td")[j].text+","+"\n")

def d3():
    driver.get("https://acupun.site/FourteenChannel/HT.html")
    ap_3 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_3 = driver.find_elements_by_tag_name("tr")
    with open ('three.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,11):
            if i == 10:
                f.write(ap_3[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_3[i].find_elements_by_tag_name("td")[j].text+","+"\n")

def d4():
    driver.get("https://acupun.site/FourteenChannel/TE.html")
    ap_4 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_4 = driver.find_elements_by_tag_name("tr")
    with open ('four.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,25):
            if i == 24:
                f.write(ap_4[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_4[i].find_elements_by_tag_name("td")[j].text+","+"\n")
      
def d5():
    driver.get("https://acupun.site/FourteenChannel/PC.html")
    ap_5 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_5 = driver.find_elements_by_tag_name("tr")
    with open ('five.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,11):
            if i == 10:
                f.write(ap_5[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_5[i].find_elements_by_tag_name("td")[j].text+","+"\n")

def d6():
    driver.get("https://acupun.site/fourteenchannel/li.html")
    ap_6 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_6 = driver.find_elements_by_tag_name("tr")
    with open ('six.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,22):
            if i == 21:
                f.write(ap_6[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_6[i].find_elements_by_tag_name("td")[j].text+","+"\n")

def d7():
    driver.get("https://acupun.site/FourteenChannel/CV.html")
    ap_7 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_7 = driver.find_elements_by_tag_name("tr")
    with open ('seven.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,25):
            if i == 24:
                f.write(ap_7[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_7[i].find_elements_by_tag_name("td")[j].text+","+"\n")

def d8():
    driver.get("https://acupun.site/FourteenChannel/SP.html")
    ap_8 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_8 = driver.find_elements_by_tag_name("tr")
    with open('eight.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,22):
            if i == 21:
                f.write(ap_8[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_8[i].find_elements_by_tag_name("td")[j].text+","+"\n")

def d9():
    driver.get("https://acupun.site/FourteenChannel/BL.html")
    ap_9 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_9 = driver.find_elements_by_tag_name("tr")
    with open ('nine.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,69):
            if i == 68:
                f.write(ap_9[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_9[i].find_elements_by_tag_name("td")[j].text+","+"\n")

def d10():
    driver.get("https://acupun.site/FourteenChannel/KI.html")
    ap_10= driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_10 = driver.find_elements_by_tag_name("tr")
    with open ('ten.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,29):
            if i == 28:
                f.write(ap_10[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_10[i].find_elements_by_tag_name("td")[j].text+","+"\n")

def d11():
    driver.get("https://acupun.site/fourteenchannel/gb.html")
    ap_11 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_11 = driver.find_elements_by_tag_name("tr")
    with open ('eleven.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,46):
            if i == 45:
                f.write(ap_11[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_11[i].find_elements_by_tag_name("td")[j].text+","+"\n")

def d12():
    driver.get("https://acupun.site/FourteenChannel/LR.html")
    ap_12 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_12 = driver.find_elements_by_tag_name("tr")
    with open ('twelve.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,16):
            if i == 15:
                f.write(ap_12[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_12[i].find_elements_by_tag_name("td")[j].text+","+"\n")

def d13():
    driver.get("https://acupun.site/fourteenchannel/st.html")
    ap_13 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_13 = driver.find_elements_by_tag_name("tr")
    with open('thirteen.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,47):
            if i == 46:
                f.write(ap_13[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_13[i].find_elements_by_tag_name("td")[j].text+","+"\n")

def d14():
    driver.get("https://acupun.site/FourteenChannel/DU.html")
    ap_14 = driver.find_element_by_tag_name("table").find_element_by_tag_name("tbody")
    ap_14 = driver.find_elements_by_tag_name("tr")
    with open('fourteen.txt', 'w', encoding='UTF-8') as f:
        for i in range(1,29):
            if i == 28:
                f.write(ap_14[i].find_elements_by_tag_name("td")[0].text)
            else:
                for j in range(5):
                    f.write(ap_14[i].find_elements_by_tag_name("td")[j].text+","+"\n")

if __name__ == '__main__':
    print(d1())
    print(d2())
    print(d3())
    print(d4())
    print(d5())
    print(d6())
    print(d7())
    print(d8())
    print(d9())
    print(d10())
    print(d11())
    print(d12())
    print(d13())
    print(d14())
    
    
driver.quit()
