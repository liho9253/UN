# -*- coding: utf-8 -*-
import cv2
import cv2 as cv
import numpy as np
 
image = cv2.imread(".\img\h9.jpg",cv.IMREAD_GRAYSCALE)
image = cv2.resize(image, (550, 730))
imgContour = image.copy()

binary = cv.adaptiveThreshold(image,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,25,15)
se = cv.getStructuringElement(cv.MORPH_RECT,(1,1))
se = cv.morphologyEx(se,cv.MORPH_CLOSE,(2,2))
mask = cv.dilate(binary,se)
# cv.imshow("image",image)
 
mask1 = cv.bitwise_not(mask)
binary =cv.bitwise_and(image,mask)
result = cv.add(binary,mask1)

a, b=cv2.findContours(result, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

for cnt in a:
    cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 4)
    print(cnt)
# cv.imshow("reslut",mask)
cv.imshow("imgContour",imgContour)
# cv.imwrite("reslut00.jpg",mask)
cv.waitKey(0)
cv.destroyAllWindows()
