import cv2
import mediapipe

handimg = cv2.imread(".\img\h7.jpg")
handimg = cv2.resize(handimg, (550, 730))
imgC = handimg.copy()

# handimg = handimg[250:480, 120:420]
handimg = cv2.cvtColor(handimg, cv2.COLOR_BGR2GRAY)
Ghandimg = cv2.GaussianBlur(handimg, (15, 15), 0)
canny = cv2.Canny(handimg, 150, 100)
adimg = cv2.adaptiveThreshold(Ghandimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 2)

edged = cv2.dilate(adimg, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
# img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
# img_gray = cv2.medianBlur(img_gray, 5)
# output = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# for cnt in contours:
#     cv2.drawContours(imgC, cnt, -1, (255, 0, 0), 4)
#     area = cv2.contourArea(cnt)
        
#     if area > 500:
#         peri = cv2.arcLength(cnt, True)
#         vertices = cv2.approxPolyDP(cnt, peri*0.02, True)
#         print(len(vertices))

# print(contours)

# cv2.imshow("show", handimg)
# cv2.imshow("canny", canny)
# cv2.imshow("gauss", Ghandimg)
cv2.imshow("adimg", adimg)
cv2.waitKey(0)
