# -*- coding: utf-8 -*-
import cv2
import cv2 as cv
import numpy as np
 
image = cv.imread(".\img\h8.jpg",cv.IMREAD_GRAYSCALE)
image = cv2.resize(image, (550, 730))
binary = cv.adaptiveThreshold(image,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,25,15)
se = cv.getStructuringElement(cv.MORPH_RECT,(1,1))
se = cv.morphologyEx(se,cv.MORPH_CLOSE,(2,2))
mask = cv.dilate(binary,se)
cv.imshow("image",image)
 
mask1 = cv.bitwise_not(mask)
binary =cv.bitwise_and(image,mask)
result = cv.add(binary,mask1)
cv.imshow("reslut",result)
cv.imwrite("reslut00.jpg",result)
cv.waitKey(0)
cv.destroyAllWindows()
