import cv2 as cv

src = cv.imread("123.png")

gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
gaussian = cv.GaussianBlur(gray, (3, 3), 0)

edges = cv.Canny(gaussian, 50, 150)
# 尋找輪廓
contours, hierarchy = cv.findContours(
    edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# 繪製輪廓
cv.drawContours(src, contours, 45, (0, 0, 255), 2)

cv.imshow('test2', src)
cv.waitKey(0)
