import cv2 
img = cv2.imread(".\img\h17.jpg")
img = cv2.resize(img, (550, 730))   
img = img[270:450, 0:150]
image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(image, 127, 255, 0)
# cv2.imshow('1', thresh)
Gauss = cv2.GaussianBlur(image, (11, 11), 0)
Canny = cv2.Canny(Gauss, 150, 200)
# a, b = cv2.findContours(Canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# imgContour = img.copy()

# # cv2.drawContours(imgContour, b, -1, (0, 255, 0), 2)

# # displayIMG(coins, Coins)

# a, b=cv2.findContours(Canny, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

# for cnt in a:
#     cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 4)
#     print(cnt)




cv2.imshow('imgContour', Canny)
# cv2.imshow('img', image)
# cv2.imshow('Canny', Canny)
cv2.waitKey(0)

