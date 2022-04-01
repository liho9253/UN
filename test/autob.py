# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time


with open("information.txt", 'w', encoding = 'utf-8') as f:
    for i in range(1,338):
        res = requests.get("http://yibian.hopto.org/acu/?ano=" + str(i))
        res.encoding = 'utf-8'
        
        
        soup = BeautifulSoup(res.text, "html.parser")
        mane = ""
        
        try:
            
            # t1 = soup.find(text = '類別').text
            # print(t1)
            
            for t in soup.find_all("span", attrs={'text':'類別'}):
                print(t)
            
    
        except AttributeError:
            break 
        
    
    
    
       
    
        time.sleep(2)


