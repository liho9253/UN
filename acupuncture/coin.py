from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def midpoint(ptA, ptB):
    return ((ptA[0]+ptB[0])*0.5, (ptA[1]+ptB[1])*0.5)

# 构造解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("-w", "--width", required=True, help="width of the left-most object in the image(in inches)")
args = vars(ap.parse_args())

# # 导入图片转换为灰度图，并进行轻微的模糊
image = cv2.imread(".\img\h8.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# 执行边缘检测
# 然后在物体之间的边缘执行膨胀+腐蚀操作使其缝隙闭合
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# 在边缘图中查找轮廓
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# 从左往右对轮廓进行排序
# 初始化'pixels per metric' 校准变量
(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None

# 分布遍历这些轮廓
for c in cnts:
    # 如果轮廓不够大，直接忽略
    if cv2.contourArea(c)<100:
        continue
    
    # 计算轮廓的选择框
    orig = image.copy()
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    
    # 对轮廓点进行排序，顺序为左上，右上，右下和左下
    # 然后绘制旋转边界框的轮廓
    box = perspective.order_points(box)
    cv2.drawContours(orig, [box.astype("int")], -1, (0,255,0), 2)
    
    # 遍历原始点并绘制出来
    for (x, y) in box:
        cv2.circle(orig, (int(x), int(y)), 5, (0,0,255), -1)
        # 打开有序的边界框，然后计算左上和右上坐标之间的中点，
  # 再计算左下和右下坐标之间的中点
    (tl, tr, br, bl) = box
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)
    
    # 计算左上点和右上点之间的中点
    # 然后是右上角和右下角之间的中点
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)
    
    # 在图中画出中点
    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
    
    # 在中点之间绘制线
    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
      (255, 0, 255), 2)
    cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
      (255, 0, 255), 2)  
# 计算中点间的欧式距离
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
    # 计算物体的大小
    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric
       
    # 在图中画出物体的大小
    cv2.putText(orig, "{:.1f}in".format(dimA),
      (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
      0.65, (255, 255, 255), 2)
    cv2.putText(orig, "{:.1f}in".format(dimB),
      (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
      0.65, (255, 255, 255), 2)
 
  # 显示输出图片
    cv2.imshow("Image", orig)
    cv2.waitKey(0)
     
    # 如果pixels per metric还未初始化，
      # 则将其计算为像素与提供的度量的比率（本例中为英寸）
    if pixelsPerMetric is None:
      pixelsPerMetric = dB / args["width"]
        
    