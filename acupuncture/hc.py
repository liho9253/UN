import cv2
import numpy as np

m = '.\img\h4.jpg' #圖片名稱
m0 = cv2.imread(m, 1) #抓取圖片
m0 = cv2.resize(m0, (550, 700))
m1 =cv2.cvtColor(m0, cv2.COLOR_BGR2GRAY) #圖片轉詼諧
m2=cv2.Canny(m1,200,250) #二極化
m3=cv2.dilate(m2, np.ones((4,4))) #膨脹
m4=cv2.erode(m3, np.ones((4,4))) #侵蝕
m5=cv2.erode(m4, np.ones((2,2))) #第二次侵蝕
a, b=cv2.findContours(m5, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #取得輪廓資料
x, y, h, w =cv2.boundingRect(a[0]) #取得包覆指定輪廓點的最小正矩形
m6 = m0[y:y+h, x: x+w] #裁切所需要的範圍
# n = m + '_zoom.jpg'
# cv2.imwrite(f"./{n}", m6) #檔案儲存

cv2.imshow('M', m6)
cv2.waitKey(0)
cv2.destroyAllWindows()