import cv2 

img = cv2.imread(".\img\h20.jpg")
h, w = img.shape[0], img.shape[1]
neww = 550
newh = 730

if w / h >= neww / newh:
    img = cv2.resize(img, (neww, int(h * neww / w)))
else:
    img = cv2.resize(img, (int(w * newh / h), newh))
    
if h > w:
    img = img[250:490, 0:190]
else:
    img = img[120:300, 0:190]

image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
Gauss = cv2.GaussianBlur(image, (3, 3), 0)
Canny = cv2.Canny(Gauss, 10, 100)

a, b=cv2.findContours(Canny, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

   
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
thresh = cv2.dilate(Canny, kernel)
thresh = cv2.erode(thresh, kernel)
closed = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE, kernel, iterations=5)
opened = cv2.morphologyEx(closed,cv2.MORPH_OPEN, kernel, iterations=5)

max_area = 0
for cnt in a:
    x, y, w, h =cv2.boundingRect(cnt)
    rec = cv2.rectangle(opened,(x, y), (x + w, y + h), (255, 255, 0), 2)
    
coinlen = w / 96 * 25.4
    
#十塊錢直徑為2.6公分


cv2.imshow('imgContour', rec)
print(coinlen)
print(w)
cv2.waitKey(0)

