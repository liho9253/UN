import cv2
import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageFont

#用於給圖片新增中文字元
def ImgText_CN(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):  #判斷是否為OpenCV圖片型別
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(r'C:\Windows\Fonts\simsun.ttc', textSize, encoding="utf-8")          ##中文字型
    draw.text((left, top), text, textColor, font=fontText)     #寫文字
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

#實現圖片反色功能
def PointInvert(img):
    height, width = img.shape        #獲取圖片尺寸
    for i in range(height):
        for j in range(width):
            pi = img[i, j]
            img[i, j] = 255 - pi
    return img



img=cv2.imread(".\img\h7.jpg",0)                #載入彩色圖
img1=cv2.imread(".\img\h7.jpg",1)               #載入灰度圖

img = cv2.resize(img, (550, 730))          #載入彩色圖
img1=cv2.resize(img1, (550, 730))

img = cv2.GaussianBlur(img, (15, 15), 0) 
img1 = cv2.GaussianBlur(img1, (15, 15), 0)    
  
recimg = img[250:480, 120:420]                #擷取需要的部分
img2 = img1[250:480, 120:420]             #擷取需要的部分
# ret, th = cv2.threshold(recimg, 90, 255, cv2.THRESH_BINARY)         #閾值操作二值化
kernel = np.ones((5, 5), np.uint8)
# canny邊緣檢測
edges = cv2.Canny(recimg, 30, 70) 
th = cv2.adaptiveThreshold(recimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
th = cv.morphologyEx(th, cv.MORPH_OPEN, kernel)
res=PointInvert(th)                           #顏色反轉
#顯示圖片
cv2.imshow('original', res)                       #顯示二值化後的圖，主題為白色，背景為黑色 更加容易找出輪廓
key = cv2.waitKey(0)
if key==27: #按esc鍵時，關閉所有視窗
    print(key)
    cv2.destroyAllWindows()
    
contours, hierarchy = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)       #得到輪廓

cnt = contours[0]               #取出輪廓

x, y, w, h = cv2.boundingRect(cnt)         #用一個矩形將輪廓包圍

img_gray = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)               #將灰度轉化為彩色圖片方便畫圖

cv2.line(img_gray, (x, y), (x, y + h), (0,0,255), 2, 5)         #上邊緣
cv2.line(img_gray, (x + w, y), (x + w, y + h), (0, 0, 255), 2, 5)    #下邊緣
cv2.line(img_gray, (x, y), (x + w, y), (0,0,255), 2, 5)      
cv2.line(img_gray, (x, y + h), (x + w, y + h), (0, 0, 255), 2, 5)  
img1[250:480, 120:420] = img_gray                                  #用帶有上下輪廓的圖替換掉原圖的對應部分

res1=ImgText_CN(img1, '寬度%d'%h, 25, 25, textColor=(0, 255, 0), textSize=30)    #繪製文字
#顯示圖片 
cv2.imshow('original', res1)
key = cv2.waitKey(0)
if key==27: #按esc鍵時，關閉所有視窗
    print(key)
    cv2.destroyAllWindows()