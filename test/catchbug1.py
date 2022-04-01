# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 20:04:39 2022

@author: Leo
"""
import requests
from bs4 import BeautifulSoup
import time


path2 = "catchbug1.txt"
with open(path2, 'w', encoding = 'utf-8') as f:
    f.write("")

for i in range(1,16):
    j = 1
    
    while(True):
        
        mane = ""
        
        if i < 10 and j < 10:
            res = requests.get("https://www.zenheart.com.tw/Meridian0" + str(i) + "_0" + str(j) + ".php")
        
        elif i < 10 and j >= 10 :
            res = requests.get("https://www.zenheart.com.tw/Meridian0" + str(i) + "_" + str(j) + ".php")

        elif i >= 10 and j < 10 :
            res = requests.get("https://www.zenheart.com.tw/Meridian" + str(i) + "_0" + str(j) + ".php")
        
        else:
            res = requests.get("https://www.zenheart.com.tw/Meridian" + str(i) + "_" + str(j) + ".php")
        
        res.encoding = 'utf-8'
        
        try:         
            soup = BeautifulSoup(res.text, "html.parser")
            mane = soup.find(class_="h3 g-color-black text-uppercase mb-2").text
            time.sleep(1)
            for mane2 in soup.find_all(class_="g-brd-around g-brd-gray-light-v4 g-brd-2 g-line-height-1_8 g-pa-30 g-mb-30", limit=4):
                mane = mane + mane2.get_text()
        except AttributeError:
            break    
        
        
        
        
        j = j + 1 
        
        with open(path2, 'a', encoding = 'utf-8') as f:
            f.write(str(mane) + "\n")

        time.sleep(2)


